from django.shortcuts import render, redirect
from django.http import HttpResponse
from community.forms import *


# Create your views here.
def index(request):
    return HttpResponse('<h1>Hellow World</h1>')


def write(request):
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            form.save()
        return redirect('list')
    else:
        form = Form()
        return render(request, 'write.html', {'form': form})


def list(request):
    articleList = Article.objects.all()
    return render(request, 'list.html', {'articleList': articleList})


def view(request, num="1"):
    article = Article.objects.get(id=num)
    return render(request, 'view.html', {'article': article})


def edit(request, num="1"):
    article = Article.objects.get(id=num)
    form = Form(request.POST or None, instance=article)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
        return redirect('list')
    else:
        return render(request, 'edit.html', {'form': form})
