
from django.contrib import admin
from .models import Profile, Address

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number")
    list_filter = ("address__city","user__is_staff")
    search_fields = ("user__username", "phone_number")

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("user", "street", "city", "postal_code")
    list_filter = ("city",)
    search_fields = ("user__username", "street", "city")
