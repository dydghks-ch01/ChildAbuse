"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from students import views  # students 앱에서 views를 임포트
from danger import views as danger_views



urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('students.urls')),
    path('', include('check.urls')),
    path('',include('danger.urls')),
    path('',include('report.urls')),
    # path('login/',include('login.urls')),
    path("accounts/", include('accounts.urls')),
    path('manage_form/', views.manage_form, name='manage_form'),  # 'manage_form' URL 패턴 추가
    path('manage_form/manage.html', views.manage_form_view, name='manage_form'),
    path('manage/', views.manage_view, name='manage'),  # manage.html로 연결되는 경로
    path('manage_form/', views.manage_form_view, name='manage_form'),
    path('danger/', danger_views.predict_abuse, name='predict_abuse'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
