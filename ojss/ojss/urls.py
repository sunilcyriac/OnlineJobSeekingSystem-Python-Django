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
    path("search", views.search, name='search'),
    path("job_details/<int:jid>",views.job_details, name="job_details"),
    path("apply/<int:jid>", views.apply, name='apply'),
    path("see_applications", views.my_applications, name="my_applications"),
    path("seeker_register",views.seekerRegister, name='seeker_register'),
    path("recruiter_register", views.recruiterRegister, name='recruiter_register'),
    path("^search?", views.search_for_jobs, name="search_list"),
    path("seekerprofile",views.seekerProfile, name= 'seeker_profile'),
    path("recruiterprofile",views.recruiterProfile, name='recruiter_profile'),
    path("skills",views.skills, name='skills'),
    path("add_jobs", views.add_job, name='add_job'),
    path("manage_jobs", views.manage_jobs, name='manage_jobs'),
    path('job_edit/<int:id>', views.edit_job, name='job_edit'),
    path('applications/<int:id>',views.applications, name='applications'),
    path('applicant_details/<int:jid>/<int:sid>',views.applicant_details, name='applicant_details'),
    path('accept_applicant/<int:aid>',views.accept_applicant, name='accept_applicant'),
    path('reject_applicant/<int:aid>',views.reject_applicant, name='reject_applicant'),
    path('logout', views.logout_user, name='logout'),
    path('ajax/load_subcategory',views.subcategory, name='subcategory'),
    path('interview_call/<int:aid>', views.interview_call, name='send_interview_call'),
    path('ajax/load_category', views.category, name='category')
]

#change add_jobs and job_edits