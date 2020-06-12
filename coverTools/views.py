from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import RegisterForm
from blog.models import Post
# Create your views here.
def homepage(request):
    return render(request, 'coverTools/homepage.html', {'pagename':'Home',})

def register(request):
    if request.method=="POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'coverTools/register.html', {'pagename':'Register','form':form})

def login(request, user):
    return HttpResponse("Login page, coverTools")

def user_details(request, username):
    #posts = reversed(Post.objects.all().filter(author=request.user.username).order_by('published_date'))
    return render(request, 'coverTools/user_details.html', {'pagename':username,})
