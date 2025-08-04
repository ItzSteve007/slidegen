from django.shortcuts import render
import random
# Create your views here.
def login(request):
    return render(request, 'login.html', {'page' :'login'})

