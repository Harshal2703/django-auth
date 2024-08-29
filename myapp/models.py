from django.db import models




class Unverified_User(models.Model):
    unverified_username = models.CharField(max_length=100)
    unverified_email = models.CharField(max_length=100)
    unverified_password = models.CharField(max_length=100)
    verifyKey = models.CharField(max_length=100)


class Forgot_Pass(models.Model):
    email = models.CharField(max_length=100)
    verifyKey = models.CharField(max_length=100)

class UserInfo(models.Model):
    email = models.CharField(max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True)

