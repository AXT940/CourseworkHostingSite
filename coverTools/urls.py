from django.urls import path
from . import views

app_name='coverTools'
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register')
]
