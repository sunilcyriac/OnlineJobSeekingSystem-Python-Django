"""ojss URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from ojss_app import views
from  django.contrib.auth.views import login

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index, name='index'),
    path("search", views.search),
    path("job_details",views.job_details, name="job_details"),
    path("apply", views.apply),
    path("see_applications", views.my_applications),
    path("see_applicants", views.applicatns),
    path("seeker_register",views.seekerRegister, name='seeker_register'),
    path("recruiter_register", views.recruiterRegister, name='recruiter_register'),
    path("^search?", views.my_applications, name="search_list"),
    path("seekerprofile",views.seekerProfile, name= 'seeker_profile')
]
