from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout

from .models import Profile
from .forms import MobileAuthForm
from .bankid import *

import os
from datetime import datetime
import qrcode
from user_agents import parse


img_src = ""

def auth_root(request):
    if request.META['HTTP_USER_AGENT']:

        ua_string = request.META['HTTP_USER_AGENT']
        user_agent = parse(ua_string)
        if user_agent.is_pc:
            return redirect("bankid_sign:auth-root-pc")
            # for testing
            # return redirect("bankid_sign:auth-root-mobile")

        else:
            return redirect("bankid_sign:auth-root-mobile")

    else:
        return HttpResponse(status = 404)


def auth_root_pc(request):
    if request.user.is_authenticated:
        return render(request,'bankid_sign/authSuccess.html')

    if request.META['HTTP_USER_AGENT']:

        ua_string = request.META['HTTP_USER_AGENT']
        user_agent = parse(ua_string)
        if user_agent.is_pc == False:
            return redirect("bankid_sign:auth-root-mobile")

    
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        end_user_ip = x_forwarded_for.split(',')[0]
    else:
        end_user_ip = request.META.get('REMOTE_ADDR')
    
    rp_response = auth(end_user_ip)

    order_ref = rp_response['orderRef']

    auto_start_token = rp_response['autoStartToken']
    qr_data = "bankid:///?autostarttoken="+auto_start_token

    img = qrcode.make(qr_data)  
    qr_dir = 'auth-qr/qr' + '-' + str(end_user_ip) + '.png'
    qr_dir = qr_dir.strip()

    with open('static/' + qr_dir, 'wb') as f:
        print(f.name)
        img.save(f)

    global img_src
    img_src = "/static/"+qr_dir
  
    context = {
        "order_ref":order_ref,
        "img_src": img_src,
    }

    return render(request, "bankid_sign/auth_root_pc.html", context)

def auth_root_mobile(request):
    if request.user.is_authenticated:
        return render(request,'bankid_sign/authSuccess.html')
    
    if request.META['HTTP_USER_AGENT']:

        ua_string = request.META['HTTP_USER_AGENT']
        user_agent = parse(ua_string)
        if user_agent.is_pc:
            return redirect("bankid_sign:auth-root-pc")

    if request.method == "POST":
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            end_user_ip = x_forwarded_for.split(',')[0]
        else:
            end_user_ip = request.META.get('REMOTE_ADDR')
        
        mobileAuthForm = MobileAuthForm(request.POST)

        if mobileAuthForm.is_valid():
            pnr = mobileAuthForm.cleaned_data['pnr']

            rp_response = auth(end_user_ip, pnr = pnr)

            order_ref = rp_response['orderRef']

            context = {
                "order_ref":order_ref
            }

            return render(request, "bankid_sign/auth_root_mobile_status.html", context)
 
    else:
        mobileAuthForm = MobileAuthForm()

    context = {
        'mobileAuthForm': mobileAuthForm,
    }

    return render(request, "bankid_sign/auth_root_mobile.html", context)

def collect_status(request, order_ref):
    global img_src

    rp_response = collect(order_ref)
    if rp_response['status'] == "complete":
        pnr = rp_response['completionData']['user']['personalNumber']
        first_name = rp_response['completionData']['user']['givenName']
        last_name = rp_response['completionData']['user']['surname']

        try:
            user = User.objects.get(username = pnr)
        except:
            user = User.objects.create(username = pnr, first_name = first_name, last_name = last_name)
            Profile.objects.create(user = user, is_verified = True)
            
        login(request, user)

        print("Got this:" , img_src)
        qr_dir = img_src.lstrip("/")
        os.remove(qr_dir)
    
        return HttpResponse(status = 202)

    elif rp_response['status'] == "pending":
        return HttpResponse(status = 201)
    
    elif rp_response['status'] == "failed":
        print("Got this:" , img_src)
        qr_dir = img_src.lstrip("/")
        os.remove(qr_dir)

        return HttpResponse(status = 205)

def auth_home(request):
    return render(request,'bankid_sign/authSuccess.html')

def auth_failed(request):
    return render(request,'bankid_sign/authFailed.html')

def auth_logout(request):
    logout(request)
    return redirect('bankid_sign:auth-root')