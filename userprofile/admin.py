from django.contrib import admin
from userprofile.models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class AffiliationAdmin(admin.ModelAdmin):
    fields = (('name', 'description'),)
    list_display = ('name', 'description')
         
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'

class UserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Affiliation, AffiliationAdmin)
    
    
    

