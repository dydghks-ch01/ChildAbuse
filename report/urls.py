
from django.urls import path
from report import views

urlpatterns = [
    path('',views.home, name='home'),
    path('report/',views.report, name='report'),
]