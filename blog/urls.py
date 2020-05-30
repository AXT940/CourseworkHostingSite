from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='post_index'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.new_post, name='new_post'),
]
