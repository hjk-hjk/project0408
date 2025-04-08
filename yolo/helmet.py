import torch
from ultralytics import YOLO
import cv2
import numpy as np

# 1. 모델 불러오기
model = YOLO('saved_model.pt')

# 2. 이미지 불러오기
img = cv2.imread('sample2.PNG')

# 3. 이미지에서 객체 탐지 (신뢰도 0.3 이상만 출력)
results = model(img, conf=0.3)

# 4. 결과 처리
for box in results[0].boxes:
    xyxy = box.xyxy[0].cpu().numpy()
    conf = box.conf[0].cpu().numpy()
    cls = int(box.cls[0].cpu().numpy())

    # 신뢰도가 0.3 이상인 경우에만 처리
    if conf > 0.3:
        label = f"Helmet {conf:.2f}"

        # 박스를 그립니다.
        cv2.rectangle(img, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]),
                                                          int(xyxy[3])), (0, 0, 255), 2)

        # 텍스트를 출력합니다.
        cv2.putText(img, label, (int(xyxy[0]), int(xyxy[1]) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

# 5. 결과 이미지 보기
cv2.imshow('Detected Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 6. 탐지된 이미지를 저장할 수 있습니다.
cv2.imwrite('detected_sample.jpg', img)