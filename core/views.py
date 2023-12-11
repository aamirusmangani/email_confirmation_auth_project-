from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.views import View
from .models import Profile
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.core.mail import send_mail
from django.conf import settings
import uuid
# Create your views here.

def index(request):
    form = LoginForm()
    return render(request, 'login.html', {'form': form})

def send_email_after_registration(email, token):
    subject = "Verify Your an Account"
    message = f"Hi, click on the link to verify your account / http://127.0.0.1:8000/account-verify/{token}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)
    

class RegisterNewUser(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'signup.html', {'form':form})
    
    def post(self, request):
        form = SignUpForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            uid = uuid.uuid4()
            pro_obj = Profile(user=user, token=uid)
            pro_obj.save()
            send_email_after_registration(user.email, token=uid)
            messages.success(request, "Your Account Created Succesfully, To Verify Your Account check your email.")
            return redirect('login')
        # else:
        #     form = SignUpForm()
        # return render(request, 'signup.html', {'form':form})
        
        
def account_verify(request, token):
    data = Profile.objects.get(token = token)
    data.verify = True
    data.save()
    messages.success(request,"Your Account has been verified!")
    return redirect('login')

class LoginUser(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form':form})
    
    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            pd = Profile.objects.get(user=user)
            if pd.verify:
                login(request, user)
                return redirect('login')
            else:
                messages.warning(request, "Your account is not verified, Please check your Mail!")
                return redirect('login')