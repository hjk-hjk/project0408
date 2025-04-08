from django.shortcuts import render, redirect, get_object_or_404
from board.form import BoardForm
from board.models import Board

# 함수를 만드는 영역(render, redirect,save..)
def  board_list(request):
    board=Board.objects.all()
    context = {"boards": board}
    return render(request, "board_list.html",context)


def  board_form(request):
    if request.method == "POST":
        form = BoardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/board_list/')
        else:
            form = BoardForm()
    else:
        form = BoardForm()
    context = {'form':form}
    return render(request, "board_form.html",context)


def  board_delete(request,pk):
    board=get_object_or_404(Board, pk=pk)
    board.delete()
    return redirect('board_list')


def  board_edit(request,pk):
    board=get_object_or_404(Board,pk=pk)
    if request.method == "POST":
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            form.save()
            return redirect('/board_list/')
        else:
            form = BoardForm(instance=board)
    else:
        form = BoardForm(instance=board)
    context = {'form':form}
    return render(request, "board_edit.html",context)