import random
import string
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser
from shared_app.models import BaseModel
from django.utils import timezone
from django.utils.timezone import timedelta
from django.core.validators import FileExtensionValidator
from rest_framework_simplejwt.tokens import RefreshToken




class AUTH_TYPE(models.TextChoices):
    email = 'email', 'Email'
    phone = 'phone', 'Phone'
    
class AUTH_STATUS(models.TextChoices):
    new = 'new', 'New'
    done = 'done', 'Done'

class GENDER(models.TextChoices):
    male = 'male', 'Male'
    female = 'female', 'Female'

class PROVINCES(models.TextChoices):
    tashkent = 'Tashkent', 'Tashkent'
    andijon = 'Andijon', 'Andijon'
    buxoro = 'Buxoro', 'Buxoro'
    fargana = 'Farg\'ona', 'Farg\'ona'
    jizzax = 'Jizzax', 'Jizzax'
    namangan = 'Namangan', 'Namangan'
    navoiy = 'Navoiy', 'Navoiy'
    qashqadaryo = 'Qashqadaryo', 'Qashqadaryo'
    samarqand = 'Samarqand', 'Samarqand'
    sirdaryo = 'Sirdaryo', 'Sirdaryo'
    surxondaryo = 'Surxondaryo', 'Surxondaryo'
    qoraqalpogiston = 'Qoraqalpog\'iston', 'Qoraqalpog\'iston'
    foreign = 'foreign', 'Foreign'
    

class CustomUser(AbstractUser, BaseModel):
    '''username, first_name, last_name, email, phone_number, date_joined, photo, date_of_birth, gender, auth_type, province, bio'''
    username = models.CharField(null=True, unique=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    province = models.CharField(choices=PROVINCES.choices, null=True, blank=True)
    email = models.EmailField(null=True, unique=True, blank=True)
    phone_number = models.CharField(max_length=13, unique=True, null=True, blank=True)
    photo = models.ImageField(upload_to='users_pictures/', default='users_pictures/default_photo.png',
                              validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'heif', 'svg'])])
    date_of_birth = models.DateField(editable=True, null=True, blank=True)
    gender = models.CharField(choices=GENDER.choices, null=True, blank=True)
    auth_type = models.CharField(choices=AUTH_TYPE.choices, default=AUTH_TYPE.email)
    auth_status = models.CharField(choices=AUTH_STATUS.choices, default=AUTH_STATUS.new)

    def __str__(self):
        return self.username
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def hashing_password(self):
        if not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)
    
    def create_verify_code(self, verify_type):
        code = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        CustomUserConfirmation.objects.create(user_id=self.id, verify_type=verify_type, code=code)
        return code
            
    
    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }




class CustomUserConfirmation(BaseModel): # 😀
    '''verify_type, code, user, expiration_time, is_confirmed'''
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='verify_code')
    code = models.CharField(max_length=4)
    verify_type = models.CharField(choices=AUTH_TYPE.choices, max_length=7)
    expiration_time = models.DateTimeField(null=True)
    is_confirmed = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.user.__str__())
    
    def save(self, *args, **kwargs):
        if self.verify_type == AUTH_TYPE.email:
            self.expiration_time = timezone.now() + timedelta(minutes=5)
        else:
            self.expiration_time = timezone.now() + timedelta(minutes=2)
        super(CustomUserConfirmation, self).save(*args, **kwargs)
        
        
        
class Note(BaseModel):
    '''owner, text, created_time, updated_time'''
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notes', null=True)
    text = models.TextField()
    
    def __str__(self):
        return f"{self.owner} {self.text}"
        
        
        
        
        
        