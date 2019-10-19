from django.shortcuts import render, redirect
from .forms import NameForm,staffform
from django.urls import reverse
from django.core.mail import send_mail
from cuqueue.models import detail
import datetime
from django.contrib.auth import authenticate,login
from django.contrib import messages
import random,string
import pyqrcode
import numpy as np
import pandas as pd


min_ch=0
q_no=0
hrs=8
def qrcode(token,name):
    q=pyqrcode.create(token)
    q.png("cuqueue/static/pics/%s.png"%name,scale=6)
    return '%s.png'%name

def index(request):
    form = NameForm()
    return render(request, "cuqueue/home.html", {"form": form})


def get_data(request):
    global min_ch, q_no,hrs
    if min_ch>59:
        hrs+=1
        min_ch=0
    q_no += 1
    min_ch = min_ch + 5
    to_give_time = datetime.datetime.now()
    to_give_time = to_give_time.replace(hour=hrs, minute=min_ch, second=0, microsecond=0)
    form = NameForm(request.POST)
    save_it = form.save(commit=False)
    save_it.check=False
    save_it.given_time = to_give_time
    save_it.lineno = q_no
    subject = "Token Number"
    random_token=''.join(random.choice(string.ascii_lowercase+string.ascii_uppercase+string.digits)for _ in range(10))
    message = "Your Token Number is:" + random_token
    from_email = 'cucoderarmy@gmail.com'
    save_it.QR=qrcode(random_token,save_it.name)
    messages.success(request,'%s.png'%save_it.name)

    to_email = [save_it.email, from_email]
    send_mail(subject, message, from_email, to_email)
    save_it.save()
    return redirect(reverse("index"))


def lists(request):
    get_it = detail.objects.all()
    return render(request, "cuqueue/list.html", {"get_it": get_it})

def login_page(request):
    form=staffform()
    password_reset='password_reset'
    return render(request,"cuqueue/staff_login.html",{'form':form,'password_reset':password_reset})

def staff(request):
    username=request.POST['username']
    password=request.POST['password']
    user=authenticate(request,username=username,password=password)
    if user is not None:
        login(request,user)
        return lists(request)

    else:
        return redirect(reverse('login'))

def reset(request):
    global min_ch,q_no
    data = detail.objects.all()
    data.delete()
    return redirect('index')
