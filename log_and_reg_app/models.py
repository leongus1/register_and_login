from django.db import models
import re
import datetime


class UserManager(models.Manager):
        
    def user_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name'])<2:
            errors['first_name']="First Name should be at least 2 characters long."
        if len(postData['last_name'])<2:
            errors['last_name']="Last Name should be at least 2 characters long."
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid Email Address."
        if not postData['password']==postData['conf_pw']:
            errors['password_match']="Password and confirmation password do not match."
        if len(postData['password'])<8:
            errors['password']="Password should be at least 8 characters."      
    
        birthdate = datetime.datetime.strptime(postData['birthdate'], "%Y-%m-%d")   
        today = datetime.datetime.now()
        age = today.year - birthdate.year -((today.month, today.day)<(birthdate.month, birthdate.day))     
        
        if age<13:
            errors['age']="You must be at least 13 years old to register."

        return errors

# Create your models here.
class Users(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birthdate = models.DateField()
    email = models.EmailField()
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
    

    
    
    