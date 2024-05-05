from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..models import YQuestion
from ..forms import YQuestionForm
from .yolo_answer_views import *
from .yolo_predict import *
from .gmail import *


def yolo_process(request, src_imgfile, yolo_question, user, chk_mail):
    # 1. list 페이지 보여주기 <== 현재 작동하고 있지 않음..
    context = {'page': 1}
    render(request, 'yolo/yolo_question_list.html', context)
    # redirect('yolo:yolo_index')

    # 2. yolo predict
    # # name = yolo_predict_cli(yolo_question.imgfile, request.user)
    save_path, predict_result = yolo_predict(src_imgfile)    
    
    # 3. auto create answer
    str_imgfile = str(src_imgfile)
    str_imgfile = str_imgfile[str_imgfile.rfind('/') + 1:]
    str_imgfile = 'yolo/answer/' + save_path + '/' + str_imgfile
    
    yolo_answer_autocreate(request, yolo_question.id, str_imgfile, predict_result)   
    
    # 4. mailling
    if chk_mail == 'yes':
        title = 'RE:품질검사 결과(' + yolo_question.subject + ')'
        content = '안녕하세요. \n' + \
                '요청하신 ' + yolo_question.subject + '에 대한 예측결과를 아래와 같이 전달해 드립니다. \n' + \
                '자세한 사항은 첨부파일을 참고부탁드립니다. \n\n' + \
                predict_result + '\n\n' + \
                '감사합니다.' \
                
        writeEmail(user.email, title, content, 'media/' + str_imgfile)
    
@login_required(login_url='common:login')
def yolo_question_create(request):

    if request.method == 'POST':
        form = YQuestionForm(request.POST, request.FILES)
        if form.is_valid():
        
            yolo_question = form.save(commit=False)
            yolo_question.imgfile = request.FILES['imgfile']
            yolo_question.author = request.user
            yolo_question.create_date = timezone.now()
            yolo_question.save()

            # print(yolo_question.chk_mail) # check:yes, not check:None
            # yolo process에서 처리
            yolo_process(request, yolo_question.imgfile, yolo_question, request.user, yolo_question.chk_mail)
            
            return redirect('yolo:yolo_index')
        
        else:
            messages.error(request, '이미지 파일을 등록해야 합니다.')
            return redirect('yolo:yolo_detail', yolo_question_id=yolo_question_id)
    # List에서 요청 등록
    else:
        form = YQuestionForm()
    context = {'form': form}
    return render(request, 'yolo/yolo_question_form.html', context)

@login_required(login_url='common:login')
def yolo_question_modify(request, yolo_question_id):
    yolo_question = get_object_or_404(YQuestion, pk=yolo_question_id)

    if request.user != yolo_question.author:
        if request.user.is_superuser == False:
            messages.error(request, '수정권한이 없습니다.')
            return redirect('yolo:yolo_detail', yolo_question_id=yolo_question_id)
        
    if request.method == "POST":
        form = YQuestionForm(request.POST, instance=yolo_question)
        if form.is_valid():
            yolo_question = form.save(commit=False)
            # yolo_question.imgfile = request.FILES['imgfile']
            yolo_question.author = request.user
            yolo_question.modify_date = timezone.now()
            yolo_question.save()
            return redirect('yolo:yolo_detail', yolo_question_id=yolo_question.id)
    else:
        form = YQuestionForm(instance=yolo_question)

    context = {'form': form}
    return render(request, 'yolo/yolo_question_modify_form.html', context)

@login_required(login_url='common:login')
def yolo_question_delete(request, yolo_question_id):
    yolo_question = get_object_or_404(YQuestion, pk=yolo_question_id)
    if request.user != yolo_question.author:
        messages.error(request, '삭제권한이 없습니다.')
        return redirect('yolo:yolo_detail', yolo_question_id=yolo_question.id)
    yolo_question.delete()
    return redirect('yolo:yolo_index')
