from gc import get_objects
from django.db import connection
from django.db.models.fields import return_None
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation.trans_real import translation

from college.models import Student, Enrol,Course


def  student_list(request):
    SQL = """
        select sno, sname, year, dept from college_student
    """
    results = Student.objects.raw(SQL)
    li = []
    for rs in results:
        li.append({
            "sno": rs.sno,
            "sname": rs.sname,
            "year": rs.year,
            "dept": rs.dept
        })
    context = {
        "li" : li,

    }
    return render(request, "student_list.html",context)


def  student_enrol(request):
    SQL = """
    SELECT id,s.sno as ssno,sname,dept,year,cno_id as ccno,grade, midterm,gimal 
    FROM COLLEGE_ENROL e join COLLEGE_STUDENT s on s.sno=e.sno_id
    """
    results = Enrol.objects.raw(SQL)
    li = []
    for rs in results:
        li.append({
            "id": rs.id,
            "sno": rs.ssno,
            "sname": rs.sname,
            "dept": rs.dept,
            "year": rs.year,
            "cno": rs.ccno,
            "grade": rs.grade,
            "midterm": rs.midterm,
            "gimal": rs.gimal,
        })
    context = {
        "li" : li,

    }
    return render(request, "student_enrol.html",context)

def  student_course(request):
    totalcount=0
    SQL = """
    SELECT id,s.sno as ssno,sname,c.dept as sdept,cname,credit,prname,year,
    c.cno as ccno,grade, midterm,gimal 
    FROM COLLEGE_ENROL e join COLLEGE_STUDENT s on s.sno=e.sno_id join COLLEGE_COURSE c 
    on e.cno_id=c.cno
    """
    results = Enrol.objects.raw(SQL)
    totalcount=len(results)
    li = []
    for rs in results:
        li.append({
            "id": rs.id,
            "sno": rs.ssno,
            "sname": rs.sname,
            "dept": rs.sdept,
            "cname": rs.cname,
            "credit": rs.credit,
            "prname": rs.prname,
            "year": rs.year,
            "cno": rs.ccno,
            "grade": rs.grade,
            "midterm": rs.midterm,
            "gimal": rs.gimal,
        })
    context = {
        "li" : li,
        "totalcount":totalcount
    }
    return render(request, "student_course.html",context)


def  s_c_e(request):
    # join 시 중복 컬럼의 별칭은 필수
    SQL = """
    SELECT id ,e.sno_id esno, s.sno ssno,c.cno ccno, e.cno_id ecno 
    FROM COLLEGE_ENROL e join COLLEGE_STUDENT s on s.sno=e.sno_id join COLLEGE_COURSE c 
    on e.cno_id=c.cno
    """
    results = Enrol.objects.raw(SQL)
    totalcount=len(results)
    li = []
    for rs in results:
        li.append({
            "id": rs.id,
            "ssno": rs.ssno,
            "esno": rs.esno,
            "ccno": rs.ccno,
            "ecno": rs.ecno,

        })
    context = {
        "li" : li,
        "totalcount":totalcount
    }
    return render(request, "s_c_e.html",context)

def  subquery1(request):
    # join 시 중복 컬럼의 별칭은 필수
    SQL = """
    select id, midterm, gimal from college_enrol where sno_id = (
    select sno from college_student where sname='나연묵'
    )
    """
    results = Enrol.objects.raw(SQL)
    totalcount=len(results)
    li = []
    for rs in results:
        li.append({
            "id": rs.id,
            "midterm": rs.midterm,
            "gimal": rs.gimal,
                    })
    context = {
        "li" : li,
        "totalcount":totalcount
    }
    return render(request, "subquery1.html",context)


from django.db import connection, transaction
from django.shortcuts import redirect
import logging

logger = logging.getLogger(__name__)
def  subquery2(request):
    def update_college_enrol():
        SQL = """
            UPDATE college_enrol
            SET midterm = midterm + 1, gimal = gimal + 1
            WHERE sno_id = (
                SELECT sno
                FROM college_student
                WHERE sname = '나연묵'
            )
        """
        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute(SQL)
                    logger.info("Update query executed successfully.")
        except Exception as e:
                logger.error(f"Error executing update query: {str(e)}")
    update_college_enrol()
    return redirect('/subquery1')


def student_form(request):
    if request.method =="POST":
        sno=request.POST.get("sno")
        sname = request.POST.get("sname")
        year = request.POST.get("year")
        dept = request.POST.get("dept")
        '''
                SQL = """
                    insert into college_student(sno,sname,year,dept)
                    values(%s,%s,%s,%s)
                """
                
                    with transaction.atomic():
                        with connection.cursor() as cursor:
                            cursor.execute(SQL,[sno,sname,year,dept])
                            return redirect('student_list')
                                    '''
        student = Student(sno=sno, sname=sname, year=year, dept=dept)
        student.save()
        return redirect('student_list')

    else:

        return render(request, "student_form.html")