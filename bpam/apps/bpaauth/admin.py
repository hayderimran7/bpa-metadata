from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin

from .models import BPAUser


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = BPAUser
        fields = ('title',)


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = BPAUser


class BPAUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'project', 'affiliations', 'first_name', 'last_name', 'email', 'is_staff')

    list_filter = ('groups', 'last_name')
    fieldsets = UserAdmin.fieldsets + (('Note', {'fields': ('note',)}),)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'project', 'email', 'telephone', 'affiliations')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
        ('Note', {'fields': ('note',)})
    )


admin.site.register(BPAUser, BPAUserAdmin)


    
    
    

