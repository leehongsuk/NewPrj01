from django.shortcuts import render
from community.forms import *


# Create your views here.
def write(request):
    form = Form()
    return render(request, 'write.html', {'form': form})


def list(request):
    articleList = Article.objects.all()
    return render(request, 'list.html', {'articleList': articleList})
