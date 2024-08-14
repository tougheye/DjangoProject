from django.contrib import admin
from django.urls import path
from .views import signup_view, login_view, user_list, user_detail, update_user, delete_user

urlpatterns = [
    path('signup/',signup_view,name='signup'),
    path('login/',login_view,name='login'),
    path('users/',user_list,name='user_list'),
    path('users/<str:username>/',user_detail,name='user_detail'),
    path('users/update/<str:username>/', update_user,name='update_user'),
    path('users/delete/<str:email>/', delete_user, name='delete_user')
]