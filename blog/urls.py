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
]
