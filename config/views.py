from  django.http  import  HttpResponse
from django.shortcuts import render, redirect


'''
def  main(request):
    return HttpResponse("안녕 하세요, pyburger 입니다. ")

def  burger_list(request):
    return HttpResponse("파이버거 목록보기")
'''


def  main(request):
    return render(request, "main.html")


def  top(request):
    return render(request, "top.html")


def  bottom(request):
    return render(request, "bottom.html")
