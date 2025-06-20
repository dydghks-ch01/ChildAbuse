from django.contrib import admin
from django.urls import path
from . import views

#add1_로그인구현법
urlpatterns = [
    path('login/', views.login, name='login'),
    path('login/', views.goLoginHtml, name='go_login_html'),
    path('signup/', views.signup, name='signup'),
    path("register/", views.registerMember, name='accounts_register'),
    path('logout/', views.logout, name='logout'),  # 로그아웃 경로 추가
    path('danger/', views.predict_abuse, name='predict_abuse'),
]
#add2