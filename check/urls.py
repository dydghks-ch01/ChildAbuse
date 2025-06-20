#add1_일일위험구현법
from django.urls import path
from check import views

urlpatterns = [
    path('check/',views.check, name='check'),
    path('check/survey1/',views.survey1, name='survey1'),
    path('check/survey2/',views.survey2, name='survey2'),
    path('check/survey3/',views.survey3, name='survey3'),
    path('check/result/',views.result, name='result'),
    path('check/detail/',views.detail, name='detail'),
]
#add2