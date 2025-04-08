from gc import get_objects

from django.shortcuts import render, redirect, get_object_or_404

from burgers.form import BurgerForm
from burgers.models import Burger


def  burger_list(request):
    burgers=Burger.objects.all()
    context = {"burgers": burgers}
    return render(request, "burger_list.html",context)


def  burger_search(request):
    keyword = request.GET.get("keyword")
    if keyword is not None :
        burgers = Burger.objects.filter(name__contains=keyword)
    else:
        burgers = Burger.objects.none()
    context = {"burgers": burgers}
    return render(request, "burger_search.html",context)


def  burger_form(request):
    if request.method == "POST":
        form = BurgerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/burger_list/')
        else:
            form = BurgerForm()
    else:
        form = BurgerForm()
    context = {'form':form}
    return render(request, "burger_form.html",context)


def  burger_delete(request,pk):
    burgers=get_object_or_404(Burger, pk=pk)
    burgers.delete()
    return redirect('burger_list')



def  burger_edit(request,pk):
    burger=get_object_or_404(Burger,pk=pk)
    if request.method == "POST":
        form = BurgerForm(request.POST, instance=burger)
        if form.is_valid():
            form.save()
            return redirect('/burger_list/')
        else:
            form = BurgerForm(instance=burger)
    else:
        form = BurgerForm(instance=burger)
    context = {'form':form}
    return render(request, "student_edit.html",context)
