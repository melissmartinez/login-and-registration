from django.db import models
from django.contrib import messages
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validator(self, data):
        errors = {}
        if len(data['fname'])<2:
            errors['fname'] = "Name is too short"
        if len(data['lname'])<2:
            errors['lname'] = "Name is too short"
        if not EMAIL_REGEX.match(data['email']):
            errors['email'] = "Email is invalid"
        if len(data['password'])<8:
            errors['password']= "Password needs to be 8 characters or longer"
        if data['password']!=data['cpassword']:
            errors['password'] = "Passwords do not match"
        return errors

    

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager() #must have this



