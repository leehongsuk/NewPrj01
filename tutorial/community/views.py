from django.shortcuts import render
from tutorial.community.forms import *


# Create your views here.
def write(request):
    form = Form()
    return render(request, 'write.html', {'form': form})

