from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='post_index'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.new_post, name='new_post'),
    path('post/edit/<int:pk>/', views.post_edit, name='edit_post'),
    path('post/delete/<int:pk>/', views.delete_post, name='delete_post'),
    path('post/new/<int:pk>/comment/', views.new_comment, name="new_comment"),
    path('post/delete/<int:pk>/comment/<int:comment_pk>/', views.delete_comment, name="delete_comment"),
    path('post/edit/<int:pk>/comment/<int:comment_pk>/', views.edit_comment, name="edit_comment"),
    path('<str:username>/drafts/', views.post_drafts, name="post_drafts"),
    path('<str:username>/drafts/<int:pk>/edit/', views.draft_edit, name='draft_edit'),
    path('<str:username>/drafts/<int:pk>/delete/', views.draft_delete, name="draft_delete"),
    path('post/<int:pk>/publish/<str:username>/', views.publish, name="publish"),
]
