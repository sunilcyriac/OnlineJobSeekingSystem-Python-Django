from  django import  forms
from  django.forms import ModelForm
from  django.contrib.auth.forms import  UserCreationForm
from  django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User,SeekerProfile,RecruiterProfile,SeekerSkillset,Job,Category,Subcategory, Interview, Application



class SeekerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True,max_length=255)


    class Meta:
        model = User
        fields = (
            'email',
            'password1',
            'password2'
        )


    def save(self, commit=True):
        user = super(UserCreationForm,self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])
        user.is_seeker = True
        user.is_recruiter = False

        if commit:
            user.save()


        return  user


class RecruiterRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True,max_length=255)

    class Meta:
        model = User

        fields = (
            'email',
            'password1',
            'password2'

        )


    def save(self, commit=True):
        user = super(UserCreationForm,self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])
        user.is_seeker = False
        user.is_recruiter = True

        if commit:
            user.save()

        return  user



class SeekerProfileForm(forms.Form):


    class Meta:
        model = SeekerProfile

    GENDER_CHOICES = [
        ('M', 'MALE'),
        ('F', 'FEMALE'),
    ]

    first_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class' : 'profile-form-style'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'profile-form-style'}))
    gender = forms.ChoiceField(label='Gender',choices=GENDER_CHOICES,widget=forms.TextInput(attrs={'class' : 'profile-form-style'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class' : 'profile-form-style'}))
    phone = forms.IntegerField(widget=forms.TextInput(attrs={'class' : 'profile-form-style'}))
    birthDate = forms.DateTimeField(widget=forms.TextInput(attrs={'class' : 'profile-form-style'}))
    current_job_role = forms.CharField(widget=forms.TextInput(attrs={'class' : 'profile-form-style'}))
    current_company = forms.CharField(widget=forms.TextInput(attrs={'class' : 'profile-form-style'}))



class RecruiterProfileForm(forms.Form):


    class Meta:
        model = RecruiterProfile

    GENDER_CHOICES = [
        ('M', 'MALE'),
        ('F', 'FEMALE'),
    ]

    first_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'profile-form-style'}))
    last_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'profile-form-style'}))
    gender = forms.ChoiceField(label='Gender', choices=GENDER_CHOICES,
                               widget=forms.TextInput(attrs={'class': 'profile-form-style'}))
    company_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'profile-form-style'}))
    company_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'profile-form-style'}))
    company_phone = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'profile-form-style'}))
    job_role = forms.CharField(widget=forms.TextInput(attrs={'class': 'profile-form-style'}))



class SkillForm(forms.Form):

    class Meta:
        model = SeekerSkillset

    skill_1 = forms.CharField(max_length=255)
    skill_2 = forms.CharField(max_length=255, required=False)
    skill_3 = forms.CharField(max_length=255, required=False)
    skill_4 = forms.CharField(max_length=255, required=False)
    skill_5 = forms.CharField(max_length=255, required=False)



class CreateJobForm(forms.Form):


    AD_CHOICES = [
        ('Y', 'YES'),
        ('N', 'NO'),
    ]

    class Meta:
        model = Job

    job_role = forms.CharField(max_length=255)
    job_description = forms.CharField(max_length=255, widget=forms.Textarea)
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    sub_category = forms.ModelChoiceField(queryset=Subcategory.objects.all())
    organization = forms.CharField(max_length=255)
    remuneration = forms.IntegerField()
    location = forms.CharField(max_length=255)
    skill_required_1 = forms.CharField(max_length=255)
    skill_required_2 = forms.CharField(max_length=255)
    skill_required_3 = forms.CharField(max_length=255, required=False)
    skill_required_4 = forms.CharField(max_length=255,required=False)
    skill_required_5 = forms.CharField(max_length=255, required=False)
    deadline = forms.DateField()
    job_ad_flag = forms.ChoiceField(label='ad_choices', choices=AD_CHOICES)



class InterviewForm(forms.Form):

    class Meta:
        model = Interview

    interview_Date = forms.DateField()
    interview_description = forms.CharField(max_length=1000)




class Application_form(forms.Form):

    class Meta:
        model = Application
        field = ('cv', 'cover_letter')


    cv = forms.CharField(max_length=1000, widget=forms.Textarea)
    cover_letter = forms.CharField(max_length=1000, widget=forms.Textarea)


