from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class UserInfo(models.Model):
    objects = models.Manager()
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    emp_id = models.CharField(unique=True, auto_created=True, blank=True, null=True, max_length=255)
    name = models.CharField(max_length=128, blank=True, null=True)
    profile_picture = models.ImageField(blank=True, null=True)
    contact = models.CharField(max_length=128, blank=True, null=True)
    designation = models.CharField(max_length=128, blank=True, null=True)
    # user_id = models.IntegerField(default=0)
    salary = models.CharField(max_length=15, blank=True, null=True)
    is_approved = models.NullBooleanField(blank=True, null=True)
    invalid_login_attempts = models.IntegerField(default=0)
    last_invalid_time = models.DateTimeField(blank=True, null=True)




