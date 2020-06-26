from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils import timezone
from django.http import HttpResponse
from django.core.paginator import Paginator

from .forms import PostForm, DeletePostForm, CommentForm, DeleteCommentForm
from .models import Post, Comment
# Create your views here.

def index(request):
    posts = Post.objects.all().exclude(published_date = None).order_by('-published_date')
    pages = Paginator(posts, 10) #page of 10 posts each
    page_number = request.GET.get('page')
    objs_for_page = pages.get_page(page_number)
    return render(request, 'blog/post_index.html', {'posts':objs_for_page, 'pagename':'Blog', 'paginator':pages})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.post_comments.all
    return render(request, 'blog/post_detail.html', {'post':post, 'pagename':'Post ' + str(post.id), 'comments':comments, 'num_of_comments':post.post_comments.count, 'delete_comment':False, 'edit_comment':False,})

def new_post(request):
    #form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('/blog/post/'+ str(post.pk) + '/', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/new_post.html', {'form':form})

def post_edit(request, pk):
        post = get_object_or_404(Post, pk=pk)
        if request.method == "POST":
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('/blog/post/'+ str(post.pk) + '/', pk=post.pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form, 'pagename':'Edit', 'edit_comment':False,})

def delete_post(request, pk):
    form = DeletePostForm()
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = DeletePostForm(request.POST)
        if form.is_valid():
            post.delete()
            return redirect('blog:post_index')
    return render(request, 'blog/post_detail.html', {'post':post, 'form':form, 'pagename':'Delete Post', 'delete':True})

def new_comment(request, pk):
    form = CommentForm()
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.published_date = timezone.now()
            comment.post = post
            comment.save()
            return redirect('blog:post_detail', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {'form':form, 'post':post, 'pagename':'New Comment', 'new_comment_writ':True})

def delete_comment(request, comment_pk, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.post_comments.all
    if request.method == "POST":
        form = DeleteCommentForm(request.POST)
        if form.is_valid() and form.cleaned_data.get('delete_confirm'):
            comment = get_object_or_404(Comment, pk=comment_pk)
            comment.delete()
            return redirect('blog:post_detail', pk=pk)
    else:
        form = DeleteCommentForm()
    return render(request, 'blog/post_detail.html', {'form':form, 'post':post, 'pagename':'Delete Comment', 'delete_comment':True, 'edit_comment':False, 'num_of_comments':post.post_comments.count, 'comments':comments, 'comment_deleting_pk':comment_pk})

def edit_comment(request, comment_pk, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.post_comments.all
    comment_to_edit = get_object_or_404(Comment, pk=comment_pk)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment_to_edit)
        if form.is_valid():
            form.save(commit=False)
            comment_to_edit.author = request.user
            comment_to_edit.published_date = timezone.now()
            comment_to_edit.save()
            return redirect('blog:post_detail', pk=pk)
    else:
        form = CommentForm(instance=comment_to_edit)
    return render(request, 'blog/post_detail.html', {'form':form, 'post':post, 'pagename':'Edit Comment', 'edit_comment':True, 'delete_comment':False, 'num_of_comments':post.post_comments.count, 'comments':comments, 'comment_to_edit_pk':comment_pk,})

def post_drafts(request, username):
    drafts = Post.objects.filter(published_date__isnull=True).filter(author=request.user)
    return render(request, 'blog/post_drafts_index.html', {'drafts':drafts, 'pagename':'Drafts', 'edit_draft':False, 'delete_draft':False})

def draft_edit(request, username, pk):
    drafts = Post.objects.filter(published_date__isnull=True).filter(author=request.user)
    draft_to_edit = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=draft_to_edit)
        if form.is_valid():
            form.save(commit=False)
            draft_to_edit.author = request.user
            draft_to_edit.save()
            return redirect('blog:post_drafts', username=username)
    else:
        form = PostForm(instance=draft_to_edit)
    return render(request, 'blog/post_drafts_index.html', {'form':form, 'drafts':drafts, 'pagename':'Edit Draft', 'edit_draft':True, 'delete_draft':False, 'draft_to_edit_pk':pk})

def draft_delete(request, username, pk):
    drafts = Post.objects.filter(published_date__isnull=True).filter(author=request.user)
    draft_to_delete = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = DeletePostForm(request.POST)
        if form.is_valid() and form.cleaned_data.get('delete_confirm'):
            draft_to_delete.delete()
            return redirect('blog:post_drafts', username=username)
    else:
        form = DeletePostForm()
    return render(request, 'blog/post_drafts_index.html', {'form':form, 'drafts':drafts, 'pagename':'Delete Draft', 'edit_draft':False, 'delete_draft':True, 'draft_to_delete_pk':pk})

def publish(request, username, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog:post_detail', pk=pk)
