from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout

from .models import Profile
from .bankid import *

import time
import hmac
import qrcode
import hashlib

def auth_root(request):
    if request.user.is_authenticated:
        return render(request,'bankid_sign/authSuccess.html')
    
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        end_user_ip = x_forwarded_for.split(',')[0]
    else:
        end_user_ip = request.META.get('REMOTE_ADDR')

    pnr = "199803093179"
    text = "Test Signing to verify user"
    rp_response = auth(pnr, end_user_ip)

    auto_start_token = rp_response['autoStartToken']
    order_ref = rp_response['orderRef']
    qr_data = "bankid:///?autostarttoken="+auto_start_token

    img = qrcode.make(qr_data) 

    with open('static/auth-qr/qr.png', 'wb') as f:
        img.save(f)

    return render(request, "bankid_sign/auth_root.html", {"order_ref":order_ref})

def collect_status(request, order_ref):
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
    context = {
        #'rp_response':rp_response,
        #'user': user,
    }

    return render(request,'bankid_sign/authSuccess.html', context)

def auth_logout(request):
    logout(request)
    return redirect('bankid_sign:auth-root')