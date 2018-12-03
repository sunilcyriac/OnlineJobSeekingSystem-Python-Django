from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import  auth,messages
from .forms import ( SeekerRegistrationForm, RecruiterRegistrationForm,
    SeekerProfileForm, RecruiterProfileForm,SkillForm, CreateJobForm, Application_form )
from .models import ( SeekerProfile,User,RecruiterProfile,SeekerSkillset,Job,Application,Message,
                      Category,Subcategory, Interview )
from django.contrib.auth import logout as django_logout
from difflib import SequenceMatcher
import datetime




def seekerRegister(request):

    if request.method == 'POST':
        form  = SeekerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')


    else:

        form = SeekerRegistrationForm

    args = {'form':form}

    return  render(request,'registration/seekerlogin.html',args)



def recruiterRegister(request):

    if request.method == 'POST':
        form  = RecruiterRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')

    else:
         form = RecruiterRegistrationForm

    args = {'form':form}

    return render(request,'registration/recruiterlogin.html',args)



def index(request):

    if request.method == "POST":
        form = AuthenticationForm(request,data=request.POST)
        email = request.POST.get('username','')
        password = request.POST.get('password','')
        if form.is_valid():
            user = auth.authenticate(username=email,password=password)

            if user is not None:
                auth.login(request,user)

                if request.user.is_recruiter:
                    try:
                        rec_profile = RecruiterProfile.objects.get(recruiter_id=request.user.id)
                        last_login = request.user.last_login
                        message_list = Message.objects.filter(recruiter_id=rec_profile.id).filter(date__gt=last_login)
                        if message_list:
                            messages.success(request, " Notification  :  You have new applications"
                                                      " for the job you posted since your last login")

                    except:
                        pass

                return render(request,'ojss_app/index.html')
        else :
            args = {'form':form}
            return render(request, 'registration/index.html', args)

    else:
        form = AuthenticationForm

    args = {'form':form}
    return  render(request,'registration/index.html', args)




def search(request):

    return render(request, 'ojss_app/index.html')


@login_required
def apply(request,jid):

    if request.method == "POST":
        form = Application_form(request.POST)
        job = Job.objects.get(id=jid)
        seekerProfile = SeekerProfile.objects.get(seeker=request.user)
        if form.is_valid():
            cv = form.cleaned_data['cv']
            cover_letter = form.cleaned_data['cover_letter']

            score = macthing_score(request,job,seekerProfile)

            application_id = Application.objects.create(

                cv  = cv,
                cover_letter= cover_letter,
                status='A',
                seeker=seekerProfile,
                matching_score=score,
                job = job,
                seeker_name=seekerProfile.first_name

            )

            application_id.save()

            job_application = Application.objects.get(id=application_id.id)

            Message.objects.create(

                application= job_application,
                recruiter = job.recruiter,
                seeker= seekerProfile,
                message_type='A',


            ).save()

            messages.success(request,"You have sucessfully applied for this position")
            args = {'form':form,
                    'job':job}
            return render(request, 'ojss_app/job_details.html', args)

        else:
            messages.warning(request,"Your application form had errors in it. Please re submit application")
            args = {'form':form,
                    'job':job,
                    'status':"T"}
            return render(request, 'ojss_app/job_details.html', args)


    else:
        raise Http404("This is an invalid request")


def macthing_score(request,job,seekerprofile):

    job_skills = [job.skill_required_1,job.skill_required_2,job.skill_required_3,
                  job.skill_required_4, job.skill_required_5]

    user_skill_object = SeekerSkillset.objects.get(seeker=seekerprofile)
    user_skills = [user_skill_object.skill_1, user_skill_object.skill_2, user_skill_object.skill_3,
                   user_skill_object.skill_4, user_skill_object.skill_5]

    score_list = []
    for item in job_skills:
        high_score = -1
        item.strip()
        if len(item) > 0:
            for user_skill in user_skills:
                score = SequenceMatcher(None, user_skill, item).ratio()
                if  score > high_score:
                    high_score = score
        if high_score != -1:
            score_list.append(high_score)


    length = len(score_list)
    total_score = 0
    for x in score_list:total_score += x
    total_score /= length
    total_score *= 100
    return total_score




@login_required
def my_applications(request):

    try:
        seekerprofile = SeekerProfile.objects.get(seeker_id=request.user.id)
        application_list = Application.objects.filter(seeker=seekerprofile).order_by('date')
        args = {'applications': application_list}

    except:
        application_list = []
        args = {'applications': application_list}

    return render(request,'ojss_app/appliedjobs.html',args)



@login_required()
def applicant_details(request,jid,sid):

    try:
        seeker = SeekerProfile.objects.get(id=sid)
        application = Application.objects.get(id=jid)
        application_status = application.status


        args = {
            'seeker' : seeker,
            'application' : application,
            'status': application_status

        }

        return render(request,'ojss_app/applicant_details.html',args)

    except SeekerProfile.DoesNotExist:
        messages.warning(request,'This User does not exist in the system any more')
        return render(request, 'ojss_app/applicant_details.html', args)

    except Application.DoesNotExist:
        messages.warning(request,'This application does not exists', args)
        return render(request, 'ojss_app/applicant_details.html', args)



@login_required
def accept_applicant(request,aid):

    try:
        application = Application.objects.get(pk=aid)

        application.status = 'S'

        sid = application.seeker_id

        jid = application.job_id

        application.save()
        seeker = SeekerProfile.objects.get(id=sid)
        application_status = application.status


        args = {
            'seeker': seeker,
            'application': application,
            'status': application_status

        }

        messages.success(request,'Applicant Selected')

        return render(request,'ojss_app/applicant_details.html', args)


    except Exception as e:


        messages.warning(request, 'Invalid Request')

        return render(request, 'ojss_app/applicant_details.html')




@login_required
def reject_applicant(request, aid):

    try:
        application = Application.objects.get(pk=aid)

        application.status = 'R'

        sid = application.seeker_id

        jid = application.job_id

        application.save()

        seeker = SeekerProfile.objects.get(id=sid)

        args = {
            'seeker': seeker,
            'application': application,
            'application_status':application.status
        }

        messages.success(request, 'Applicant Rejected')

        return render(request, 'ojss_app/applicant_details.html', args)


    except:

        messages.warning(request, 'Invalid Request')

        return render(request, 'ojss_app/applicant_details.html')


@login_required
def interview_call(request, aid):

    try:
        application = Application.objects.get(pk=aid)

        if application.status != 'I' :

            application.status = 'I'

            application.save()

            sid = application.seeker_id

            jid = application.job_id

            job = Job.objects.get(id=jid)

            Interview.objects.create(

                application = application

            ).save()


            Message.objects.create(

                message_type = 'I',
                application = application,
                recruiter = job.recruiter,
                seeker = application.seeker,

            ).save()


            seeker = SeekerProfile.objects.get(id=sid)

            args = {
                'seeker': seeker,
                'application': application,
                'application_status': application.status
            }

            messages.success(request, 'Interview Call sent')

            return render(request, 'ojss_app/applicant_details.html', args)

        else:

            messages.warning(request, 'Invalid Request')

            return render(request, 'ojss_app/applicant_details.html')


    except Exception as e:


        messages.warning(request, 'Invalid Request')

        return render(request, 'ojss_app/applicant_details.html')




@login_required
def applications(request,id):

    try:
        application_list = Application.objects.filter(job_id=id)
        args = {'applications' : application_list}
        return render(request,'ojss_app/showapplicants.html',args)

    except Application.DoesNotExist:
        return  render(request, 'ojss_app/showapplicants.html')

    except Exception as e:
        return render(request,'ojss_app/showapplicants.html')


@login_required
def job_details(request,jid):

    try:
        job = Job.objects.get(id=jid)
        seekerprofile = SeekerProfile.objects.get(seeker=request.user)
        if request.user.is_seeker:

            try:
                application = Application.objects.get(seeker=seekerprofile, job = job)
                status = application.status
                form = None


            except Exception as e:
                print(e)
                status = "T"
                form = Application_form

        else:
            status = "F"
            form = None

        args = {'job':job,
                'status':status,
                'form':form}


    except:
        messages.warning(request,"invalid request")
        args = {'job':None,
                'status':None,
                'form':None}

    return render(request,'ojss_app/job_details.html', args)



@login_required
def recruiterProfile(request):

    if request.method == 'POST':

        form = RecruiterProfileForm(request.POST)

        if form.is_valid():

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            gender = form.cleaned_data['gender']
            company_address = form.cleaned_data['company_address']
            company_phone = form.cleaned_data['company_phone']
            job_role = form.cleaned_data['job_role']
            company_name = form.cleaned_data['company_name']

            try:

                profile = RecruiterProfile.objects.get(recruiter_id=request.user.id)

                profile.first_name = first_name
                profile.last_name = last_name
                profile.gender = gender
                profile.company_address = company_address
                profile.company_phone = company_phone
                profile.job_role = job_role
                profile.company_name = company_name
                profile.save()

            except RecruiterProfile.DoesNotExist:

                RecruiterProfile.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    gender=gender,
                    company_address=company_address,
                    company_phone=company_phone,
                    job_role=job_role,
                    company_name=company_name,
                    recruiter_id=request.user.id

                ).save()

            form = RecruiterProfileForm(initial={'first_name': first_name, 'last_name': last_name,
                                              'gender': gender, 'company_address': company_address,
                                              'company_phone': company_phone,
                                              'job_role': job_role, 'company_name': company_name})
        args = {'form': form}
        return render(request, 'ojss_app/recruiterprofile.html', args)

    else:
        if request.user.is_authenticated:
            recruiter = request.user.id

            try:
                profile = RecruiterProfile.objects.get(recruiter_id=recruiter)
                first_name = profile.first_name
                last_name = profile.last_name
                gender = profile.gender
                company_address = profile.company_address
                company_phone = profile.company_phone
                job_role = profile.job_role
                company_name = profile.company_name

            except:

                first_name = ""
                last_name = ""
                gender = ""
                company_address = ""
                company_phone = ""
                job_role = ""
                company_name = ""

            # Getting user details to show in profile

            form = RecruiterProfileForm(initial={'first_name': first_name, 'last_name': last_name,
                                              'gender': gender, 'company_address': company_address,
                                              'company_phone': company_phone,
                                              'job_role': job_role, 'company_name': company_name})
            args = {'form': form}
            return render(request, 'ojss_app/recruiterprofile.html', args)




@login_required
def seekerProfile(request):

    if request.method == 'POST':

        form = SeekerProfileForm(request.POST)




        if form.is_valid():

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            gender = form.cleaned_data['gender']
            address = form.cleaned_data['address']
            phone = form.cleaned_data['phone']
            birthdate = form.cleaned_data['birthDate']
            current_job = form.cleaned_data['current_job_role']
            company = form.cleaned_data['current_company']



            try:

                profile = SeekerProfile.objects.get(seeker_id=request.user.id)


                profile.first_name = first_name
                profile.last_name = last_name
                profile.gender = gender
                profile.address = address
                profile.phone = phone
                profile.birthDate = birthdate
                profile.current_job = current_job
                profile.company = company
                profile.save()

            except SeekerProfile.DoesNotExist:

                SeekerProfile.objects.create(
                first_name = first_name,
                last_name = last_name,
                gender = gender,
                address = address,
                phone = phone,
                birthDate = birthdate,
                current_job_role = current_job,
                current_company = company,
                seeker_id=request.user.id
                ).save()


            form = SeekerProfileForm(initial={'first_name': first_name, 'last_name' : last_name ,
                                          'gender':gender,'address':address,'phone':phone,'birthDate' : birthdate,
                                          'current_job_role':current_job, 'current_company':company})
        args = {'form':form}
        return render(request, 'ojss_app/seekerprofile.html', args)

    else:
        if request.user.is_authenticated:
            seeker   = request.user.id

            try:
                profile = SeekerProfile.objects.get(seeker_id=seeker)
                first_name = profile.first_name
                last_name = profile.last_name
                gender = profile.gender
                address = profile.address
                phone = profile.phone
                birthdate = profile.birthDate
                current_job = profile.current_job_role
                company = profile.current_company

            except:

                first_name = ""
                last_name = ""
                gender = ""
                address = ""
                phone = ""
                birthdate = ""
                current_job = ""
                company = ""

        # Getting user details to show in profile



            form = SeekerProfileForm(initial={'first_name': first_name, 'last_name' : last_name ,
                                          'gender':gender,'address':address,'phone':phone,'birthDate' : birthdate,
                                          'current_job_role':current_job, 'current_company':company})
            args = {'form': form }
            return render(request, 'ojss_app/seekerprofile.html',args)




@login_required
def skills(request):

    if request.method == "POST":
        form = SkillForm(request.POST)

        if form.is_valid():


            skill_1 = form.cleaned_data['skill_1']
            skill_2 = form.cleaned_data['skill_2']
            skill_3 = form.cleaned_data['skill_3']
            skill_4 = form.cleaned_data['skill_4']
            skill_5 = form.cleaned_data['skill_5']


            try:

                seekerProfile = SeekerProfile.objects.get(seeker_id=request.user.id)

                try:

                    skills = SeekerSkillset.objects.get(seeker_id=seekerProfile.id)

                    skills.skill_1 = skill_1
                    skills.skill_2 = skill_2
                    skills.skill_3 = skill_3
                    skills.skill_4 = skill_4
                    skills.skill_5 = skill_5
                    skills.save()

                except SeekerSkillset.DoesNotExist:

                    SeekerSkillset.objects.create(

                        skill_1=skill_1,
                        skill_2=skill_2,
                        skill_3=skill_3,
                        skill_4=skill_4,
                        skill_5=skill_5,
                        seeker_id=seekerProfile.id

                    ).save()

                form = SkillForm(initial={'skill_1': skill_1, 'skill_2': skill_2, 'skill_3': skill_3,
                                          'skill_4': skill_4, 'skill_5': skill_5})
                args = {'form': form}
                return render(request, 'ojss_app/seekerskill.html', args)


            except SeekerProfile.DoesNotExist:

                messages.warning(request, 'You Must Complete Your Profile Before Editing Skills')
                form = SkillForm()
                args = {'form': form}
                return render(request, 'ojss_app/seekerskill.html', args)


        else:
            args = {'form':form}
            messages.warning(request,'Skills was not saved. There was some error in the form')
            return render(request,'ojss_app/seekerskill.html', args)





    else:

        if request.user.is_authenticated:

            try:
                seekerProfile = SeekerProfile.objects.get(seeker_id=request.user.id)
                skills = SeekerSkillset.objects.get(seeker_id=seekerProfile.id)

                skill_1 = skills.skill_1
                skill_2 = skills.skill_2
                skill_3 = skills.skill_3
                skill_4 = skills.skill_4
                skill_5 = skills.skill_5

                skills.save()

            except:

                skill_1 = ""
                skill_2 = ""
                skill_3 = ""
                skill_4 = ""
                skill_5 = ""



            form = SkillForm(initial={'skill_1': skill_1, 'skill_2': skill_2, 'skill_3': skill_3,
                                      'skill_4': skill_4, 'skill_5': skill_5})
            args = {'form': form}
            return render(request, 'ojss_app/seekerskill.html', args)




@login_required
def manage_jobs(request):

    try:
        r_profile = RecruiterProfile.objects.get(recruiter_id=request.user.id)
        job_list = Job.objects.filter(recruiter_id = r_profile.id)
        args = {'jobs': job_list}

    except:
        job_list = []
        args = {'jobs':job_list}

    return render(request,'ojss_app/managejobs.html',args)



@login_required
def add_job(request):

    if request.method == "POST":

        form = CreateJobForm(request.POST)

        if form.is_valid():

            job_role = form.cleaned_data['job_role']
            job_description = form.cleaned_data['job_description']
            job_organization = form.cleaned_data['organization']
            job_remuneration = form.cleaned_data['remuneration']
            job_location = form.cleaned_data['location']
            skill_required_1 = form.cleaned_data['skill_required_1']
            skill_required_2 = form.cleaned_data['skill_required_2']
            skill_required_3 = form.cleaned_data['skill_required_3']
            skill_required_4 = form.cleaned_data['skill_required_4']
            skill_required_5 = form.cleaned_data['skill_required_5']
            deadline = form.cleaned_data['deadline']
            job_ad_flag = form.cleaned_data['job_ad_flag']
            category = form.cleaned_data['category']
            sub_category = form.cleaned_data['sub_category']




            try:
                r_profile = RecruiterProfile.objects.get(recruiter_id=request.user.id)

                Job.objects.create(
                    job_role=job_role,
                    job_description=job_description,
                    organization=job_organization,
                    remuneration=job_remuneration,
                    location=job_location,
                    skill_required_1=skill_required_1,
                    skill_required_2=skill_required_2,
                    skill_required_3=skill_required_3,
                    skill_required_4=skill_required_4,
                    skill_required_5=skill_required_5,
                    deadline=deadline,
                    job_ad_flag=job_ad_flag,
                    category=category,
                    sub_category=sub_category,
                    recruiter_id=r_profile.id
                ).save()

                messages.success(request, 'Your Job was Created')
                return render(request,'ojss_app/createjob.html')

            except RecruiterProfile.DoesNotExist:
                messages.warning(request, 'You Must Complete Your Profile Before Creating Jobs')
                return render(request, 'ojss_app/createjob.html')


            except Exception as e:
                return render(request,'ojss_app/createjob.html',{'form':form})

        else:
            messages.warning(request, "Job creation failed. Please make sure your form is complete and error free")
            return render(request,'ojss_app/createjob.html',{'form':form})



    else:

        try :
            r_profile = RecruiterProfile.objects.get(recruiter_id=request.user.id)
            form = CreateJobForm
            args = {'form' : form}
            return  render(request,'ojss_app/createjob.html', args)

        except RecruiterProfile.DoesNotExist:
            messages.warning(request, 'You Must Complete Your Profile Before Creating Jobs')
            return render(request,'ojss_app/managejobs.html')



@login_required
def edit_job(request,id):

    if request.method == "POST":

        form = CreateJobForm(request.POST)

        if form.is_valid():

            job_role = form.cleaned_data['job_role']
            job_description = form.cleaned_data['job_description']
            job_organization = form.cleaned_data['organization']
            job_remuneration = form.cleaned_data['remuneration']
            job_location = form.cleaned_data['location']
            skill_required_1 = form.cleaned_data['skill_required_1']
            skill_required_2 = form.cleaned_data['skill_required_2']
            skill_required_3 = form.cleaned_data['skill_required_3']
            skill_required_4 = form.cleaned_data['skill_required_4']
            skill_required_5 = form.cleaned_data['skill_required_5']
            deadline = form.cleaned_data['deadline']
            category = form.cleaned_data['category']
            sub_category = form.cleaned_data['sub_category']
            job_ad_flag = form.cleaned_data['job_ad_flag']

            try:
                job = Job.objects.get(id=id)

                job.job_role = job_role
                job.job_description = job_description
                job.organization = job_organization
                job.remuneration = job_remuneration
                job.location = job_location
                job.skill_required_1 = skill_required_1
                job.skill_required_2 = skill_required_2
                job.skill_required_3 = skill_required_3
                job.skill_required_4 = skill_required_4
                job.skill_required_5 = skill_required_5
                job.deadline = deadline
                job.category = category
                job.sub_category = sub_category
                job.job_ad_flag = job_ad_flag

                job.save()


                messages.success(request, 'Your Job was Saved')
                form = CreateJobForm(initial={'job_role': job_role, 'job_description': job_description,
                                              'organization': job_organization, 'remuneration': job_remuneration,
                                              'location': job_location, 'skill_required_1': skill_required_1,
                                              'skill_required_2': skill_required_2, 'skill_required_3': skill_required_3
                    , 'skill_required_4': skill_required_4, 'skill_required_5': skill_required_5
                    , 'deadline': deadline,  'category' : category, 'sub_category': sub_category.sub_category_name
                    ,'job_ad_flag': job_ad_flag})

                args = {'form': form}

                return render(request,'ojss_app/editjob.html',args)




            except Exception as e:
                messages.warning(request, 'Job edit failed. Please make sure your form is complete and error free')
                return render(request,'ojss_app/editjob.html', {'form':form})

        else:
            messages.warning(request, "Job edit failed. Please make sure your form is complete and error free")
            return render(request,'ojss_app/editjob.html',{'form':form})



    else:

        try :

            job = Job.objects.get(pk=id)
            job_role = job.job_role
            job_description = job.job_description
            organization = job.organization
            remuneration = job.remuneration
            location = job.location
            skill_required_1 = job.skill_required_1
            skill_required_2 = job.skill_required_2
            skill_required_3 = job.skill_required_3
            skill_required_4 = job.skill_required_4
            skill_required_5 = job.skill_required_5
            category = job.category
            sub_category = job.sub_category
            deadline = job.deadline
            job_ad_flag = job.job_ad_flag


            form = CreateJobForm (initial={'job_role':job_role,'job_description':job_description,
                                           'organization':organization, 'remuneration':remuneration,
                                           'location': location, 'skill_required_1' : skill_required_1,
                                            'skill_required_2' : skill_required_2, 'skill_required_3' : skill_required_3
                                           , 'skill_required_4' : skill_required_4 , 'skill_required_5' : skill_required_5
                                           ,'deadline':deadline,
                                           'category':category, 'sub_category':
                                               sub_category.sub_category_name,'job_ad_flag':job_ad_flag})

            args = {'form' : form}
            return render(request,'ojss_app/editjob.html', args)

        except Exception as e:
            messages.warning(request, 'No Such Job Exists')
            return render(request,'ojss_app/editjob.html')


@login_required
def logout_user(request):

    django_logout(request)
    return HttpResponseRedirect('/')



def search_for_jobs(request):

    if request.method == "GET":

        keyword = request.GET.get('keyword')
        if keyword == None or keyword == "":
            args = { 'results' : None}
            messages.warning(request, "Please input a  valid keyword for search")
            return render(request,'ojss_app/index.html', args)

        search_by = request.GET.get('search_by')
        search_by_list = [1,2,3]
        if  not search_by.isnumeric() or  int(search_by) not in search_by_list:
            args = {'results': None}
            messages.warning(request, "Please select a valid value for search by")
            return render(request,'ojss_app/index.html', args)

        category = request.GET.get('category')
        if not category:
            args = {'results': None}
            messages.warning(request, "Please select a valid category")
            return render(request, 'ojss_app/index.html', args)

        subcategory = request.GET.get('subcategory')
        if not subcategory:
            args = {'results': None}
            messages.warning(request, "Please select a valid subcategory ")
            return render(request, 'ojss_app/index.html', args)

        if search_by == "1":
            result = search_by_job_role(keyword,category,subcategory)
            args = {'results':result}
            if result == None:
                messages.warning(request,"No results found for your search")
            return render(request,'ojss_app/index.html',args)



        if search_by == "2":
            result = search_by_location(keyword,category,subcategory)
            args = {'results':result}
            if result == None:
                messages.warning(request,"No results found for your search")
            return render(request,'ojss_app/index.html',args)


        if search_by == "3":
            result = search_by_remuneration(keyword,category,subcategory)
            args = {'results': result}
            if result == None:
                messages.warning(request,"No results found for your search")
            return render(request, 'ojss_app/index.html', args)



def search_by_job_role(keyword,category,subcategory):

    keyword = keyword.strip()
    today = datetime.date.today()
    db_search = Job.objects.filter(category_id=category).filter(sub_category=subcategory).\
        filter(job_role__contains=keyword).filter(job_ad_flag='Y').filter(deadline__gte=today)


    if not db_search:
        return None

    return db_search



def search_by_location(keyword,category,subcategory):

    keyword = keyword.strip()
    today = datetime.date.today()
    db_search = Job.objects.filter(category_id=category).filter(sub_category=subcategory).\
        filter(location__contains=keyword).filter(job_ad_flag='Y').filter(deadline__gte=today)

    if not db_search:
        return None

    return db_search



def search_by_remuneration(keyword,category,subcategory):

    keyword = keyword.strip()
    try:
        today = datetime.date.today()
        length = len(keyword)
        keyword = int(keyword)
        keyword_range = ( keyword, keyword+5000 )
        db_search = Job.objects.filter(category_id=category).filter(sub_category_id=subcategory)\
           .filter(remuneration__range= keyword_range).filter(job_ad_flag='Y').filter(deadline__gte=today)\
            .order_by('remuneration')
        return db_search

    except :
        return  None




def subcategory(request):
    category_id = request.GET.get('category')
    sub_category = Subcategory.objects.filter(category_id=category_id)
    return  render(request, 'ojss_app/subcategory_drop_down.html',{'sub_category':sub_category})



def category(request):
    category_list = Category.objects.all()
    return render(request,'ojss_app/category_drop_down.html', {'category':category_list})
