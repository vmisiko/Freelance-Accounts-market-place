from django.urls import path, include
from . import views

app_name = "UnlocksApp"

urlpatterns = [
    path("", views.UnlocksView.as_view(), name = "unlock"),
    path("logins/", views.LoginsView.as_view(), name = "Logins")

]