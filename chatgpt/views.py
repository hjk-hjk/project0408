import base64
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from chatgpt.models import ChatGPT
from PIL import Image  # 수정: 여기서 PIL 모듈을 올바르게 임포트
import openai
from django.conf import settings
from io import BytesIO

from dotenv import load_dotenv
import os
load_dotenv()
api_key1 = os.getenv("API_KEY1")

openai.api_key = api_key1

def chatgpt_form(request):
    if request.method == "POST" and request.FILES['file']:
        uploaded_image = request.FILES['file']

        # 이미지 파일을 올바르게 열기
        image = Image.open(uploaded_image)  # 수정: 여기서 Image.open()을 사용

        # 이미지를 바이너리 형식으로 변환
        from io import BytesIO
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='PNG')  # 이미지 형식 지정 (예: 'JPEG')
        img_byte_arr = img_byte_arr.getvalue()  # 바이트 형태로 변환

        # 이미지를 base64로 인코딩
        img_base64 = base64.b64encode(img_byte_arr).decode('utf-8')

        # OpenAI API를 사용하여 이미지 분석 요청
        response = openai.chat.completions.create(
            model="gpt-4-turbo",  # GPT-4 Vision 모델 사용
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "이 이미지에 대해 설명해주세요."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img_base64}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=300,  # 응답 길이 제한
        )

        # 결과 반환
        print("Image Analysis Result:")
        result = response.choices[0].message.content
        print(result)

        # 분석 결과를 ChatGPT 모델에 저장
        chatgpt = ChatGPT(name="이름", aiexplain="설명", file=uploaded_image)
        chatgpt.save()

        # 최근 업로드된 파일 가져오기
        filename = ChatGPT.objects.order_by('-id').values_list('file', flat=True).first()
        li = ChatGPT.objects.order_by('-id').all()

        context = {
            "result": result,
            "filename": filename,
            "li": li,
        }

        return render(request, 'chatgpt.html', context)

    else:
        # 업로드된 모든 파일 기록을 가져오기
        li = ChatGPT.objects.order_by('-id').all()
        context = {"li": li}
        return render(request, 'chatgpt.html', context)
