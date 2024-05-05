from django import forms
from yolo.models import YQuestion, YAnswer, YComment

class YQuestionForm(forms.ModelForm):
    class Meta:
        model = YQuestion
        fields = ['subject', 'content', 'imgfile', 'chk_mail']
        # widgets = {
        #     'subject': forms.TextInput(attrs={'class': 'form-control'}),
        #     'content': forms.Textarea(attrs={'class': 'form-control', 'rows':10}),
        # }
        labels = {
            'subject': '제목',
            'content': '내용',
            'imgfile': '업로드 파일',
            'chk_mail': '이메일 전송',
        }
        # help_texts = { 'chk_mail': _('체크하시면 회원가입시 등록한 이메일로 예측결과를 전송합니다.'), }

class YAnswerForm(forms.ModelForm):
    class Meta:
        model = YAnswer
        fields = ['content', 'imgfile']
        labels = {
            'content': '답변내용',
            'imgfile': '업로드 파일',
        }

class YCommentForm(forms.ModelForm):
    class Meta:
        model = YComment
        fields = ['content']
        labels = {
            'content': '댓글내용'
        }