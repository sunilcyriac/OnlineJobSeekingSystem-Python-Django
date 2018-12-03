from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager



class UserManager(BaseUserManager):

    def create_user(self,email,password=None,is_active=True,is_recruiter = False, is_seeker = False, is_staff=False, is_admin= False):

        if not email:
            raise ValueError("User must have a valid email address")

        if not password:
            raise ValueError("User must have a password")

        user_obj = self.model(

            email = self.normalize_email(email)
        )

        user_obj.set_password(password)

        user_obj.is_active = is_active

        user_obj.is_recruiter = is_recruiter

        user_obj.is_seeker = is_seeker

        user_obj.is_admin = is_admin

        user_obj.is_staff = is_staff

        user_obj.save(using=self._db)

        return  user_obj


    def create_staffuser(self,email,password):
        user = self.create_user(
            email,
            password,
            is_staff=True
        )
        return user


    def create_superuser(self,email,password=None):
        user = self.create_user(
            email,
            password,
            is_admin=True,
            is_staff=True
        )

        return user





class User(AbstractBaseUser):
    email = models.EmailField(

        verbose_name='Email Address',
        max_length=255,
        unique=True,
    )

    is_active = models.BooleanField(default=True)
    is_recruiter = models.BooleanField(default=False)
    is_seeker = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    register_Date = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    object = UserManager()

    def __str__(self):
        return  self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True



class SeekerProfile(models.Model):

    GENDER_CHOICES = (
        ('M','MALE'),
        ('F','FEMALE'),
    )

    seeker = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1,
                              choices=GENDER_CHOICES,
                              default='M')
    address = models.CharField(max_length=255)
    phone = models.IntegerField(max_length=10)
    birthDate = models.DateField()
    current_job_role = models.CharField(max_length=255)
    current_company = models.CharField(max_length=255)



    def __str__(self):
        return self.first_name


class RecruiterProfile(models.Model):

    GENDER_CHOICES = (
        ('M', 'MALE'),
        ('F', 'FEMALE'),
    )

    recruiter = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1,
                              choices=GENDER_CHOICES,
                              default='M')
    company_name = models.CharField(max_length=255)
    company_address = models.CharField(max_length=255)
    company_phone = models.IntegerField()
    job_role = models.CharField(max_length=255)

    def __str__(self):
        return self.first_name


class Category(models.Model):

    category_name = models.CharField(max_length=255)


    def __str__(self):
        return self.category_name


class Subcategory(models.Model):

    sub_category_name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.sub_category_name






class Job(models.Model):
    job_role = models.CharField(max_length=255)
    job_description = models.CharField(max_length=1000)
    organization = models.CharField(max_length=255)
    remuneration = models.IntegerField()
    location = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True)
    sub_category = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True)
    skill_required_1 = models.CharField(max_length=255)
    skill_required_2 = models.CharField(max_length=255)
    skill_required_3 = models.CharField(max_length=255, blank=True, null=True)
    skill_required_4 = models.CharField(max_length=255, blank=True, null=True)
    skill_required_5 = models.CharField(max_length=255, blank=True, null=True)
    deadline = models.DateField()
    posted_date = models.DateField(auto_now_add=True)
    job_ad_flag = models.CharField(max_length=1)
    recruiter = models.ForeignKey(RecruiterProfile,on_delete=models.CASCADE)



    def __str__(self):
        return self.job_role



class SeekerSkillset(models.Model):

    seeker = models.OneToOneField(SeekerProfile,on_delete=models.CASCADE)
    skill_1 = models.CharField(max_length=255)
    skill_2 = models.CharField(max_length=255, blank=True, null=True)
    skill_3 = models.CharField(max_length=255, blank=True, null=True)
    skill_4 = models.CharField(max_length=255, blank=True, null=True)
    skill_5 = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return self.seeker


class Application(models.Model):


    APPLICATION_CHOICES = (
        ('A', 'ACTIVE'),
        ('S', 'SELECTED'),
        ('R', 'REJECTED'),
        {'I', 'Interview'},
    )


    seeker = models.ForeignKey(SeekerProfile, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    seeker_name = models.CharField(max_length=255)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    cover_letter = models.CharField(max_length=1000)
    cv = models.CharField(max_length=1000)
    matching_score = models.IntegerField()
    status = models.CharField(max_length=1,
                              choices=APPLICATION_CHOICES,
                              default='M')



class Message(models.Model):



    message_type = models.CharField(max_length=1)
    seeker = models.ForeignKey(SeekerProfile, on_delete=models.CASCADE)
    recruiter = models.ForeignKey(RecruiterProfile,on_delete=models.CASCADE)
    application = models.ForeignKey(Application,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class Interview(models.Model):


    interview_date = models.DateTimeField(auto_now_add=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)



