from celery import shared_task
from django.http import request
# from django.core.mail import send_mail
import uuid
from django.conf import settings

from django.contrib.auth import get_user_model

from celery import shared_task
from django.core.mail import send_mail
from src import settings
from django.utils import timezone
from datetime import timedelta
from accounts.models import *
import uuid
from accounts.views import *;
from django.shortcuts import render
from django.http import request
from django.http import HttpResponse
from .views import *;


@shared_task(bind=True)
def test_func(self):
    for i in range(10):
        print(i)
    return "Done"




