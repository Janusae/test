from django.urls import path
from . import views
urlpatterns = [
    path("" , views.Index , name = "Index") ,
    path("register" , views.RegisterView.as_view() , name = "register"),
    path("login" , views.LoginView.as_view() , name = "login"),
    path("forget" , views.ForgetView.as_view() , name ="forget"),
    path("logout/<code>" , views.LogoutView.as_view() , name ="logout"),
    path("reseat-code/<code>" , views.Reseat_code.as_view() , name ="reseat_code"),
    path("active-code/<code>" , views.Active_EmailView.as_view() , name = "active_email")
]