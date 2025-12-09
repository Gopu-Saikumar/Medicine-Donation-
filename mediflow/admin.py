from django.contrib import admin
from .models import User, NGOProfile

class UserAdmin(admin.ModelAdmin):
    list_display = ("fullname", "email", "phone", "user_type")
    list_filter = ("user_type",)
    search_fields = ("email", "fullname")

admin.site.register(User, UserAdmin)


class NGOProfileAdmin(admin.ModelAdmin):
    list_display = ("ngo_name", "registration_number", "contact_person", "email")
    search_fields = ("ngo_name", "registration_number", "email")

admin.site.register(NGOProfile, NGOProfileAdmin)
