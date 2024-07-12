from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager



class Custom_user(AbstractUser):
    first_name = models.CharField(max_length=30,null=False,blank=False)
    last_name = models.CharField(max_length=30,null=False,blank=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=30)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    def __str__(self):
        return self.email
    
    @property 
    def username(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class Custom_user_OTP(models.Model):
    user = models.ForeignKey(Custom_user,on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email
    
    class Meta:
        verbose_name = 'OTP'
        verbose_name_plural = 'OTPs'
    
