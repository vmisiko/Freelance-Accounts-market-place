from django.contrib import admin
from .models import Unlocks,Logins

# Register your models here.
@admin.register(Unlocks)
class UnlocksModel(admin.ModelAdmin):

    list_display = ["user","category", "email","status" ]

@admin.register(Logins)
class LoginsModel(admin.ModelAdmin):

    list_display = ["user","category", "email","status" ]
