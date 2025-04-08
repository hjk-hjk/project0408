from http.client import responses
import requests
from django.contrib.admin.templatetags.admin_list import results
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from restfulapi.models import Student
from django.db import connection
import xml.etree.ElementTree as ET

# Create your views here.
def restful_json(request):
    from django.http import JsonResponse
    li =[
        {"name":"young","age":"12"},
        {"name": "kim", "age": "13"},
        {"name": "둘리", "age": "14"},
        ]
    context ={
        'items' : li,
        'totalcount' : 3,
        'type' : 'json',
    }
    print("==>결과값(li):",li)
    return JsonResponse(context, json_dumps_params={'ensure_ascii': False})


def restful_json_sql(request):
    from django.http import JsonResponse
    query="""
        select sno, sname,year,dept from restfulapi_student
      """
    results = Student.objects.raw(query)
    li=[]
    for rs in results:
        li.append({
            "sno" : rs.sno,
            "sname": rs.sname,
            "year": rs.year,
            "dept": rs.dept,
        })
    context ={
        'items' : li,
        'create':'hyunji',
        'yymmdd':'2025-03-11',

    }
    print("==>결과값(li):",li)
    return JsonResponse(context, json_dumps_params={'ensure_ascii': False})

def restful_txt_sql(request):
    from django.http import JsonResponse
    query="""
        select sno, sname,year,dept from restfulapi_student
      """
    results = Student.objects.raw(query)
    strli = ""
    for s in results:
        strli +=f"{s.sno},{s.sname},{s.year},{s.dept}; "
        print("====> txt results:",strli)

    type ='text/plain; charset=utf-8'
    response = HttpResponse(strli, content_type=type)

    return response


def restful_xml_sql(request):

    from django.http import HttpResponse
    query="""
        select sno, sname,year,dept from restfulapi_student
      """
    results = Student.objects.raw(query)
    root = ET.Element("response")
    records = ET.SubElement(root, "result")
    for rs in results:
        record = ET.SubElement(records, "record")

        sno = ET.SubElement(record,"sno")
        sno.text = str(rs.sno)

        sname = ET.SubElement(record, "sname")
        sname.text = str(rs.sname)

        year = ET.SubElement(record, "year")
        year.text = str(rs.year)

        dept = ET.SubElement(record, "dept")
        dept.text = str(rs.dept)

    tree = ET.ElementTree(root)
    response = HttpResponse(content=ET.tostring(root,encoding="utf-8", method='xml'),
                            content_type='application/xml;charset=utf-8')
    return response


def request_json_sql(request):

    SQL = """
    insert into requeststudent(idx, sno, sname, year, dept, today)
    values(board_idx.nextval, %s,%s,%s,%s, sysdate)
    """
    cursor = connection.cursor()

    url = 'http://127.0.0.1:8000/restful_json_sql/'
    response = requests.get(url)
    li = []
    create = ""
    yymmdd = ""
    if response.status_code == 200:
        data = response.json()
        results = data.get("items",[])
        create = data.get("create")
        yymmdd = data.get("yymmdd")


        for rs in results:
            li.append({
                "sno":rs.get('sno'),
                "sname": rs.get('sname'),
                "year":rs.get('year'),
                "dept": rs.get('dept'),
                      })

            cursor.execute(SQL, [rs.get('sno'), rs.get('sname'), rs.get('year'), rs.get('dept')])
        cursor.close()
    else:
        print("에러코드:",response.status_code)
    record_count=len(li)
    context={
        "results": li,
        "record_count": record_count,
        "create" : create,
        "yymmdd": yymmdd
        }
    connection.close()
    return render(request, "request_json_sql.html",context)

def request_xml_sql(request):

    SQL = """
    insert into requeststudent(idx, sno, sname, year, dept, today)
    values(board_idx.nextval, %s,%s,%s,%s, sysdate)
    """
    cursor = connection.cursor()

    url = 'http://127.0.0.1:8000/restful_xml_sql/'
    response = requests.get(url)
    li = []
    if response.status_code == 200:
        root =ET.fromstring(response.text)
        results = root.find('result').findall('record')

        for rs in results:
            sno=rs.find('sno').text
            sname=rs.find('sname').text
            year=rs.find('year').text
            dept=rs.find('dept').text


            cursor.execute(SQL, [rs.get('sno'), rs.get('sname'), rs.get('year'), rs.get('dept')])
        cursor.close()
    else:
        print("에러코드:",response.status_code)
    record_count=len(li)
    context={
        "results": li,
        "record_count": record_count,

               }
    connection.close()
    return render(request, "request_json_sql.html",context)