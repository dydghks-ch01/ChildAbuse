from django.urls import path
from danger import views

urlpatterns = [
    path('', views.home, name='home'),
    path('danger/', views.predict_abuse, name='danger'),
    # path('danger/view/', views.danger, name='danger_view'),  # 폼 뷰
]