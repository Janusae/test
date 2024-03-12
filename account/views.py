from django.contrib.auth import login , logout
from django.http import HttpRequest, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .models import User
from .form import Register_Form, Login_Form, Forget_pass_Form, Reseat_Form
from django.utils.crypto import get_random_string
from utils.email_service import send_email
# Create your views here.
def Index(request):

    return render(request , "account/Index.html" )
class RegisterView(View):
    def get(self , request):
        form = Register_Form()
        return render(request , "account/register.html" , {"form":form})
    def post(self , request : HttpRequest):
        form = Register_Form(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            user : bool = User.objects.filter(email__exact=email).exists()
            if not user :
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                new_user = User(username=username , email=email , is_active=False , email_active_code=get_random_string(94))
                new_user.set_password(password)
                send_email("فعالسازی حساب کاربری", new_user.email ,{"user":new_user} , "active-code.html")
                new_user.save()
                return redirect(reverse("Index"))
class Active_EmailView(View):
    def get(self , request , code):
        user = User.objects.filter(email_active_code__exact=code).first()
        if user is not None :
            if not user.is_active:
                user.is_active = True
                user.email_active_code = get_random_string(94)
                user.save()
                return redirect(reverse("Index"))
class LoginView(View):
    def get(self , request):
        form = Login_Form()
        return render(request , "account/login.html" , {"form" : form})
    def post(self , request : HttpRequest):
        form = Login_Form(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user :User = User.objects.filter(email__exact=email).first()
            if user:
                check = user.check_password(password)
                if check:
                    if user.is_active :
                        login(request , user)
                        return redirect(reverse("Index"))
                    else :
                        raise Http404("Your email is not active yet!")
            else :
                raise Http404("We couldn't find your email")
        else :
            raise Http404("Your Information is not valid")
class ForgetView(View):
    def get(self , request):
        form = Forget_pass_Form()
        return render(request , "account/forget.html" , {"form":form})
    def post(self , request):
        form = Forget_pass_Form(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            user : User = User.objects.filter(email__exact=email).first()
            if user is not None:
                user.email_active_code = get_random_string(94)
                user.save()
                return redirect(reverse("Index"))
            else :
                raise Http404("We couldn't find your email")
        else :
            raise Http404("Your email is not valid!")
class Reseat_code(View):
    def get(self , request , code):
        user = User.objects.filter(email_active_code__exact=code).first()
        if user is not None :
            form = Reseat_Form()
            return render(request , "account/reseat.html" , {"data":  form})
    def post(self , request , code):
        form = Reseat_Form(request.POST )
        if form.is_valid():
            user : User = User.objects.filter(email_active_code__exact=code).first()
            if user is not None:
                password = form.cleaned_data.get("password")
                user.set_password(password)
                user.email_active_code = get_random_string(94)
                user.is_active =True
                user.save()
                return redirect(reverse("Index"))
            else :
                raise Http404("We couldn't find your email")
        else :
            raise Http404("Your email is not valid!")
class LogoutView(View):
    def get(self , request , code):
        user : User = User.objects.filter(email_active_code__exact=code).first()
        if user is not None :
           logout(request)
           return redirect(reverse("Index"))



