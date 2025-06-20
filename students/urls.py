
from django.urls import path
from students import views

urlpatterns = [
    path('',views.home, name='home'),
    path('manage/',views.manage, name='manage'),
    path('manage_form/', views.manage_form, name='manage_form'),
    path('manage_register/', views.manage_register, name='manage_register'),
    path('manage_detail/', views.manage_detail, name='manage_detail'),
    path('manage_detail/<int:child_id>/', views.manage_detail, name='manage_detail'),
    path('main/',views.main, name='main'),
    # path('danger/',views.danger, name='danger'),
    # path('report/',views.report, name='report'),
    # path('login/',views.login, name='login'),
]