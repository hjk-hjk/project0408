from django.shortcuts import render
from yolo.models import Yolo
import os
from django.conf import settings
import ultralytics

ultralytics.checks()
import locale

locale.getpreferredencoding = lambda: "UTF-8"
from ultralytics import YOLO
import cv2
from PIL import Image
from datetime import datetime


# pip install ultralytics

def yolo_helmet(request):
    if request.method != "POST":
        return render(request, "yolo.html")
    else:
        modelName = 'saved_model.pt'
        img_path = os.path.join(settings.STATICFILES_DIRS[0], "model", modelName)
        model = YOLO(img_path)

        # 방법 2.
        # form 에서 이미지 가져 오기
        uploaded_image = request.FILES['file']

        upload_dir = os.path.join(settings.MEDIA_ROOT, 'yolo/original/')
        file_path = os.path.join(upload_dir, uploaded_image.name)
        os.makedirs(upload_dir, exist_ok=True)

        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_image.chunks():
                destination.write(chunk)

            # 저장한 이미지 읽기
        img = cv2.imread(file_path)

        result = model.predict(source=img)
        print(result)
        print("==>model.names : ", model.names)
        count = 0
        for box in result[0].boxes:

            if float(box.conf) > 0.3:
                x1, y1, x2, y2 = box.xyxy[0].numpy().flatten().astype(int)
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # 클래스 이름과 신뢰도 추출
                class_index = int(box.cls)
                class_name = model.names[class_index]  # 클래스 이름 가져오기
                if class_name == 'helmet':
                    count += 1
                confidence = float(box.conf)
                font = cv2.FONT_HERSHEY_SIMPLEX
                # print("==>", class_index, class_name, confidence)
                # 텍스트 출력
                cv2.putText(img, f'{class_name} {confidence:.2f}', (x1, y1 - 10), font, 0.9, (0, 255, 0), 2)

        current_time = datetime.now().strftime("%H%M%S")  # 예: 143022 (14시 30분 22초)
        result_image_name = f'result_image_{current_time}.jpg'  # 파일 이름에 시분초 추가
        save_path = os.path.join(settings.MEDIA_ROOT, 'yolo/result/', result_image_name)
        cv2.imwrite(save_path, img)

        result_img_path = os.path.join('yolo/result/', result_image_name)
        yolo = Yolo(name="영심", aiexplain=count, original_img=uploaded_image, result_img=result_img_path)
        yolo.save()

        # 원본 파일 삭제
        if os.path.exists(file_path):  # 파일이 존재하는지 확인
            os.remove(file_path)  # 파일 삭제
            print(f"Deleted: {file_path}")  # 삭제된 파일 경로 출력
        else:
            print(f"File not found: {file_path}")  # 파일이 없을 경우 메시지 출력

        original_img = yolo.original_img
        result_img = yolo.result_img

        context = {
            "original": original_img,
            "result": result_img,
            "count": count,
        }

        return render(request, 'yolo.html', context)