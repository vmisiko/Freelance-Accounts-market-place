from django.contrib import admin
from .models import Unlocks,Logins, Logins_passwords

# Register your models here.
@admin.register(Unlocks)
class UnlocksModel(admin.ModelAdmin):

    list_display = ["user","req_id","category", "email","status" ]

@admin.register(Logins)
class LoginsModel(admin.ModelAdmin):

    list_display = ["user","req_id","category", "email","status" ]

@admin.register(Logins_passwords)
class Logins_passwords_Model(admin.ModelAdmin):

    list_display = ["name", "email", "password" ]

