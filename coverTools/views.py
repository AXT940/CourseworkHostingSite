from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.core.paginator import Paginator

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password

from .forms import RegisterForm, DeleteForm
from blog.models import Post
from django.contrib.auth.models import User
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
    user_name = username
    user = User.objects.get(username=user_name)
    posts = Post.objects.all().filter(author=user).order_by('published_date')
    pages = Paginator(posts, 10) #page of 10 posts each
    page_number = request.GET.get('page')
    objs_for_page = pages.get_page(page_number)
    if len(posts) == 0:
        last_post = 'No posts created.'
    else:
        last_post = posts[0].published_date
    return render(request, 'coverTools/user_details.html', {'pagename':username, 'posts':objs_for_page, 'last_post_date':last_post, 'num_posts':len(posts), 'date_joined':user.date_joined.date(), 'paginator':pages,})

def delete_user(request, username):
    form = DeleteForm()
    if request.method=='POST':
        account = get_user(username)
        if account:
            form = DeleteForm(request.POST)
            if form.is_valid() and form.cleaned_data.get('username') == request.user.username and form.cleaned_data.get('delete_confirm') and check_password(form.cleaned_data.get('password'), request.user.password):
                #user = get_user(username)
                account.delete()
                messages.info(request, "User "+ username + " account successfully deleted!")
                return redirect('coverTools:homepage')
    else:
        form = DeleteForm()
    return render(request, 'coverTools/delete_user.html', {'pagename':'Delete '+ str(username), 'form':form, 'delete':True})

def get_user(username):
    try:
        user = User.objects.get(username=username)
        return user
    except Exception as e:
        return None
