from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def homepage(request):
    return render(request, 'coverTools/homepage.html', {'pagename':'Home'})

def login(request):
    return HttpResponse("Login page, coverTools")

def register(request):
    return HttpResponse("Register for an account, coverTools")
