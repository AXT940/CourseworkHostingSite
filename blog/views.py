from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import PostForm
from django.http import HttpResponse

from .models import Post
# Create your views here.

def index(request):
    posts = Post.objects.all().order_by('published_date')
    if not posts:
        return HttpResponse("There is no posts do view for now.")
    else :
        return render(request, 'blog/post_index.html', {'posts':posts, 'pagename':'Blog'})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post':post, 'pagename':'Post ' + str(post.id)})

def new_post(request):
    #form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('/blog/post/'+ str(post.pk) + '/', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/new_post.html', {'form':form})
