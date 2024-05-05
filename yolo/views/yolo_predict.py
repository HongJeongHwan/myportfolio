import numpy as np
from ultralytics import YOLO
from django.utils import timezone
import os


# 파일업로드시에 호출하는 함수
def yolo_predict_cli(filename, user):
    used_model = './media/yolo/models/robo_best_20240314_6class_per100.pt'
    # if os.path.exists('./yolo_media/models/robo_best_20240314_6class_per100.pt') == True:
    #     print('./yolo_media/models/robo_best_20240314_6class_per100.pt')

    # from_dir = './yolo_media/from'
    # source_file = './yolo_media/from/303_15_eb2afc35-8b99-4b1f-a746-19b70367ace5.JPG'
    source_file = './media/' + str(filename)
    # to_dir = './yolo_media/to'
    project_fld = './media/yolo/answer'
    # models의 upload_to에서 직접 지정하는 것으로 변경
    # name = timezone.now().strftime("%Y-%m-%d").replace('-','') + '_' +\
    #        str(user) + '_' + \
    #        str(filename) + '_'
    # name = timezone.now().strftime("%Y-%m-%d").replace('-','')
    # name = timezone.now().strftime("%Y%m%d%H%M%S")
    name = timezone.localtime(timezone.now()).strftime("%Y%m%d%H%M%S")

    # command = "yolo task=segment mode=predict model='./yolo_media/models/robo_best_20240314_6class_per100.pt' conf=0.15 source='./yolo_media/from/303_15_eb2afc35-8b99-4b1f-a746-19b70367ace5.JPG' project='./yolo_media/to' name='20240325' save=True"
    command = "yolo task=segment mode=predict \
        model='" + used_model + "' \
        conf=0.15 \
        source='" + source_file + "' \
        project='" + project_fld + "' \
        name='" + name + "' \
        save=True save_txt=True"
    os.system(command)
    is_success = True
    return name

# 파일업로드시에 호출하는 함수
def yolo_predict(filename):

    used_model = YOLO('./media/yolo/models/robo_best_20240314_6class_per100.pt')  # pretrained YOLOv8n model
    source_file = './media/' + str(filename)
    project_fld = './media/yolo/answer'
    
    # predict한 이미지를 저장할 경로
    save_path = timezone.localtime(timezone.now()).strftime("%Y%m%d%H%M%S")
    results = used_model.predict(source=source_file,
                                project=project_fld,
                                name=save_path,
                                save=True,
                                save_txt=False,
                                conf=0.15)
    # 예측결과
    result = results[0]
    boxes = result.boxes
    # masks = result.masks
    #key는 필요 없고 value는 필요하다.
    idx2class = np.array([value for key, value in result.names.items()])
    cls = idx2class[boxes.cls.to('cpu').numpy().astype('int')]

    print_item = ""
    # boxes 추가    
    for box in boxes:
        print_item += "- 불량항목:{}, 불량확률:{}% \n  cls: {}\n  conf: {}\n  data: {}\n  id: {}\n  is_track: {}\n  orig_shape: {}\n  shape: {}\n  xywh: {}\n  xywhn: {}\n  xyxy: {}\n  xyxyn: {}\n\n" \
            .format(idx2class[box.cls.to('cpu').numpy().astype('int')].item(), round(box.conf.item()*100, 2), \
            box.cls, box.conf, box.data, box.id, box.is_track, box.orig_shape, box.shape, box.xywh, box.xywhn, box.xyxy, box.xyxyn)
    # speed 추가
    print_item += "\n\n"
    print_item += "- Speed \n"
    print_item += "preprocess:" + str(result.speed['preprocess']) + "ms, inference:" + str(result.speed['inference']) + "ms, postprocess:" + str(result.speed['postprocess']) + " per image"
    
    return save_path, print_item
