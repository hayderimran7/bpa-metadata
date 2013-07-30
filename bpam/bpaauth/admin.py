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
    
    list_display = ('username', 'title', 'department', 'first_name', 'last_name', 'email')
    list_filter = ('groups', 'last_name')
    fieldsets = UserAdmin.fieldsets + (('Note', {'fields': ('title',)}),)


admin.site.register(BPAUser, BPAUserAdmin)


    
    
    

