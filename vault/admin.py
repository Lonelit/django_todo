from django.contrib import admin
from django.contrib.auth.password_validation import password_changed

from .models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("task", "note", "owner", "importance", "deadline")
    search_fields = ("task", "deadline")
    list_filter = ("owner",)

# Register your models here.
