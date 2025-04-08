from fileinput import filename
from http.client import responses
from io import BytesIO
import openai
from django.contrib.admin.templatetags.admin_list import results
from openai import OpenAI
from django.core.files.storage import default_storage
from django.shortcuts import render, get_object_or_404, redirect
from gc import get_objects
from PIL import Image
from google import genai
from django.conf import settings
from django.shortcuts import render
import time
from llm.models import Gemini2, ChatGPT
from dotenv import load_dotenv
import os
load_dotenv()
GPT_API_KEY1=os.getenv("GPT_API_KEY1")
GEMINI_api_key=os.getenv("GEMINI_api_key")
ALIBABA_api_key=os.getenv("ALIBABA_api_key")

gemini_api_key=GEMINI_api_key

def  gemini_txt(request):
    if request.method != "POST":
        return render(request, "gemini_txt.html")
    else:
        mf = request.POST.get("mf")
        age = request.POST.get("age")
        inter = request.POST.get("inter")
        best = request.POST.get("best")
        bb = request.POST.get("bb")
        client = genai.Client(api_key=gemini_api_key)
        response = client.models.generate_content(
            model="gemini-2.0-flash",  # 2024년 12월 출시, 학습: 2023년까지 데이터를 기반으로 학습.
            contents=f"{mf}{age}{inter}{best}{bb} 30 내외로 주식 종목 간략히 설명 부탁해.",
        )
        print(response.text)

        context = {
            "result": response.text,
        }
        return render(request, "gemini_txt.html", context)



from datetime import datetime
from django.conf import settings


def  gemini_img(request):
    client = genai.Client(api_key=gemini_api_key)
    if request.method == 'POST' and request.FILES['file']:
        uploaded_image = request.FILES['file']
        name = request.POST.get("name")
        explain = request.POST.get('explain')


        print("==>name:explain,",name,explain)

        # static/img 디렉토리 경로 설정
        dir_name = "img"
        img_name = uploaded_image.name

        # 파일 중복 체크 하기 중복이 있으면 이름 변경.
        target_dir = os.path.join(settings.STATICFILES_DIRS[0], dir_name)
        file_path = os.path.join(target_dir, img_name)
        if os.path.exists(file_path):
            timestamp = time.strftime("%H%M%S")
            name, ext = os.path.splitext(img_name)
            img_name = f"{name}_{timestamp}{ext}"


        # 파일명 으로 이미지 저장 하기
        file_path = os.path.join(target_dir, img_name)
        with open(file_path, 'wb') as f:
            for chunk in uploaded_image.chunks():
                f.write(chunk)

        # 저장된 이미지 불러 오기
        image_path = os.path.join(settings.STATICFILES_DIRS[0], dir_name, img_name)
        image = Image.open(image_path)

        content = ("100자 정도로 해서 사진설명 부탁해 그리고 사람이 몇명인지 꼭 알려줘")

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[image, content ])
        #print(response.text)
        print("===> img_name:",img_name)

        #
        gemini = Gemini2(name=name,explain=explain,aiexplain=response.text,
                         filename=img_name,file=uploaded_image)
        gemini.save()
        gemini2 = Gemini2.objects.all()
        context = {
            'result': response.text,
            'img_name':img_name,
            'results' : gemini2
        }
        return render(request, 'gemini_img.html', context)
    else :
        return render(request, 'gemini_img.html')

def  gemini_delete(request, pk):
    import os
    from django.conf import settings

    gemini = get_object_or_404(Gemini2, pk=pk)

    filename = gemini.filename  # static 파일 삭제
    file_path = os.path.join(settings.BASE_DIR,
                             'media', 'gemini', filename )
    os.remove(file_path)

    file = gemini.file    # media 파일 삭제
    file_path = os.path.join(settings.MEDIA_ROOT,
                             '', file.name)
    default_storage.delete(file_path)
    return redirect('gemini_img')



def alibaba_api(request):
    if request.method != "POST":
        return render(request, "alibaba_api.html")
    else:
        question = request.POST.get("question")
        result_context = ""
        try:
            client = OpenAI(
                # If the environment variable is not configured, replace the following line with your API key: api_key="sk-xxx",
                api_key="ALIBABA_api_key",
                base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
            )
            system_content = " 한국어(korean)만 사용할 수 있습니다. "
            user_content = f" {question}에 대해서 50자 정도로 요약 해줘"
            completion = client.chat.completions.create(
                model="qwen-plus",
                messages=[
                    {'role': 'system', 'content': system_content},
                    {'role': 'user', 'content': user_content}
                    ]
            )
            print(completion.model_dump_json())
            result_context = completion.choices[0].message.content
            print(completion.choices[0].message.content)
        except Exception as e:
            print(f"Error message: {e}")

        context = {
            "question": question,
            "result": result_context
        }

        return render(request, 'alibaba_api.html', context)
import openai
import os
from openai import OpenAI
def chatgpt_api(request):
    if request.method !="POST":
        return render(request,"chatgpt_api.html")
    else:
        question= request.POST.get("question")


    # It's better to store the API key securely (e.g., in an environment variable)

    openai.apikey = GPT_API_KEY1
    client = OpenAI(api_key=GPT_API_KEY1)
    sys_context = "당신은 최고의 애널리스트입니다"
    user_context = f"{question}현재 미국 주식 상황"
    user_context += " 100토큰으로 설명"

    response = client.chat.completions.create(
        model="gpt-4",  # You can also use gpt-3.5 if needed
        messages=[
            {'role': 'system', 'content': sys_context},
            {'role': 'user', 'content': user_context}
        ]
    )
    print(response.choices[0].message.content)
    result = response.choices[0].message.content
    context={
        "result":result
    }

    return render(request, 'chatgpt_api.html', context)


# OpenAI API 키 설정

openai.api_key = GPT_API_KEY1

def chatgpt_api_img(request):
    if request.method == "POST" and request.FILES['file']:
        uploaded_image =request.FILES['file']

        image = Image.open(uploaded_image)

        # 이미지를 바이너리 형식으로 변환
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='JPEG')  # 이미지 형식 지정 (예: 'JPEG')
        img_byte_arr = img_byte_arr.getvalue()  # 바이트 형태로 변환

        # 이미지를 base64로 인코딩
        import base64
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


        chatgpt=ChatGPT(name="이름" ,explain="설명",aiexplain="설명",file=uploaded_image)
        chatgpt.save()
        #id를 기준으로 내림차순
        filename=(ChatGPT.objects.order_by('-id').values_list('file').first())
        li = ChatGPT.objects.order_by('-id').all()
        print(filename)
        context = {
            "result": result,
            "filename":filename[0],
            "li":li

        }

        return render(request, 'result.html', context)
    else:
        li =ChatGPT.objects.order_by('-id').all()
        context = {"li": li}
        return render(request, 'result.html',context )


def  chatgpt_delete(request, pk):
    import os
    from django.conf import settings

    chatgpt = get_object_or_404(ChatGPT, pk=pk)

    filename = chatgpt.filename  # static 파일 삭제
    file_path = os.path.join(settings.BASE_DIR,
                             'media', 'chatgpt', filename )
    os.remove(file_path)

    file = chatgpt.file    # media 파일 삭제
    file_path = os.path.join(settings.MEDIA_ROOT,
                             '', file.name)
    default_storage.delete(file_path)
    return redirect('chatgpt_api_img')
