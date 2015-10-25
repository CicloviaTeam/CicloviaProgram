# coding=utf-8
from django.contrib.auth.models import User
##from django.contrib.auth.decorators import login_required

##Create user.

##def CreateU(username, email, password):
##    "Create user."
##    User.objects.create_user(username, email, password)

def CreateU(username, password):
    "Create user."
    User.objects.create_user(username, '', password)

##Delete user.
##@login_required at view
def DeleteU(pUsername):
    "Delete user."
    User.objects.get(username=pUsername).delete()

##Check if user is logged in.
def notAutheticated(User):
    return not User.is_authenticated()

