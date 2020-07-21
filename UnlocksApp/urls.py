from django.urls import path, include
from . import views

app_name = "UnlocksApp"

urlpatterns = [
    path("unlocks/", views.UnlocksView.as_view(), name = "unlock"),
    path("logins/", views.LoginsView.as_view(), name = "Logins"),
    path("", views.unlockloginView , name="unlocklogin"),
    path("unlock-post/", views.unlocks_post, name ="unlock_post"),
    path("logins-post/", views.logins_post,name ="logins_post" ),
    path("unlock_mpesa_pay/", views.Unlock_Mpesa_pay, name="unlock_mpesa_pay"),
    path("realtime_validate/", views.realtime_validate, name ="valid_pay"),
    path("validate_code", views.validate_mpesa_code, name ="validate_mpesa_code"),

]