from django.shortcuts import render, redirect
from django.urls import reverse 
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages, auth 
from django.conf import settings 


from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError



from .models import Users, Profile
from django.core.mail import EmailMessage
import random



def randomTokens():
    tokens = ''
    for i in range(6):
        val = str(random.randint(1, 9))
        tokens += val
    return tokens
        # print(val)
        # print(tokens)

code = randomTokens()

def sendToken(user, request):
    current_site = get_current_site(request)
    
    email_subject = 'Account Token'
    email_body = render_to_string(
        'mail_pages/token.html', 
        {
        'email': user,
        'domain': current_site.domain,
        'token': code,
        }
    )
    print(code)

    try:
        email = EmailMessage(
            subject=email_subject,
            body=email_body,
            from_email=settings.EMAIL_HOST_USER,
            to=[user.email]
        )
        email.content_subtype = 'html'
        email.send()

    except Exception as e:
        print('did not work')

    





def loadLoginPage(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Users.objects.filter(email=email).exists():
            print('it exists')
            try:
                user = authenticate(request, username=email)
                print(user)
            except ValueError:
                print('wrong')
            if user is not None:
                login(request, user)
                sendToken(user, request)
                print(email)
                return redirect('token')
            
            else:
                print('no')
        else:
          return redirect('signup')
        

    return render(request, 'pages/login.html')


def loadSignUpPage(request):
    if request.method == 'POST':
        names = request.POST['names']
        email = request.POST['email'] 
        dob = request.POST['dob']

        try:  
            predata = Users.objects.create_user(email=email)
            user = Profile(user=predata, fullname=names, birthday=dob)
            user.save()
            predata.save()
            print(names, dob, email)
            return redirect('login')
        except Exception as e:
            print('not working')

    return render(request, 'pages/signup.html')


def loadTokenPage(request):
    check_token = code 
    if request.method == 'POST':
        token = request.POST['token']
        if token == check_token:
            return redirect('success')
        else:
            print('not the same')
    return render(request, 'pages/token.html')


def loadSuccessPage(request):
    return render(request, 'pages/success.html')