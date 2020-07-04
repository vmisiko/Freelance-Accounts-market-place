from django.shortcuts import render
from .models import Logins, Unlocks
# Create your views here.
from django.views import generic



class UnlocksView(generic.CreateView):
    model = Unlocks
    fields = ["full_Names","category", "email", "Url" ,"other"]
    template_name = "UnlocksApp/unlock.html"

class LoginsView(generic.CreateView):
    model = Logins
    fields = ["full_Names","category", "email","other"]
    template_name = "UnlocksApp/logins.html"