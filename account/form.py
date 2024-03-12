from django import forms
from django.core.exceptions import ValidationError


class Register_Form(forms.Form):
    username = forms.CharField(label="نام کاربری" , widget=forms.TextInput())
    email = forms.EmailField(label="ایمیل" , widget=forms.EmailInput())
    password = forms.CharField(label="گذرواژه" , widget=forms.PasswordInput())
    confirm_password = forms.CharField(label="تکرار گذرواژه" , widget=forms.PasswordInput())
    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_passwrod = self.cleaned_data.get("confirm_password")
        if password == confirm_passwrod:
            return confirm_passwrod
        else :
            raise ValidationError(password , "Your password and your confirm password is not the same!")
class Login_Form(forms.Form):
    email = forms.EmailField(label="ایمیل" , widget=forms.EmailInput())
    password = forms.CharField(label="گذرواژه" , widget=forms.PasswordInput)
class Forget_pass_Form(forms.Form):
    email = forms.EmailField(label="ایمیل" , widget=forms.EmailInput())
class Reseat_Form(forms.Form):
    password = forms.CharField(label="گذرواژه" , widget=forms.PasswordInput())
    confirm_password = forms.CharField(label="تکرار گذرواژه" , widget=forms.PasswordInput())

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password == confirm_password:
            return confirm_password
        else :
            raise ValidationError(password , "Your password and confirm password is not the same")