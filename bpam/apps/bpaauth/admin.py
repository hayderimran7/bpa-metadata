from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import BPAUser


class BPAUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = BPAUser


class BPAUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = BPAUser

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            BPAUser.objects.get(username=username)
        except BPAUser.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])


class BPAUserAdmin(UserAdmin):
    form = BPAUserChangeForm
    add_form = BPAUserCreationForm

    list_display = ('username', 'project', 'first_name', 'last_name', 'email', 'is_staff')
    list_filter = ('groups', 'last_name')

    # fieldsets = UserAdmin.fieldsets + (('Note', {'fields': ('note',)}),)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'project', 'email', 'telephone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
        ('Note', {'fields': ('note',)})
    )


admin.site.register(BPAUser, BPAUserAdmin)


    
    
    

