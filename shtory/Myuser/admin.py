from django.contrib import admin
from .models import *
from .forms import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class MyUserAdmin(UserAdmin):
    list_display = ('username', 'email',  'is_staff', 'gender', 'image_tag', 'phone_number','dob')
    fieldsets = (
            ('None', {'fields' : (('username', 'email'), 'password')}),
            ('Personal Info', {'fields' : (('first_name', 'last_name'), ('gender', 'dob'),'phone_number', 'profile_pic')}),
            
            ('Permission', {
                'fields': (('is_staff', 'is_superuser', 'is_active'),'groups', 'user_permissions'),
                'classes': ('grp-collapse grp-closed',)
                }),
            ('Important Dates', {
                'fields': ('last_login', 'date_joined'),
                'classes': ('grp-collapse grp-closed',)
                })
    )
    add_fieldsets = (
            ('None', {
                'classes' : ('wide',),
                'fields': ('username', 'email', 'gender', 'dob', 'phone_number', 'passwd1', 'passwd2')
                }),)
    add_form = UserCreationForm
    search_fields = ('username', 'email')


admin.site.register(CustomUser, MyUserAdmin)
admin.site.register(Relationship)
