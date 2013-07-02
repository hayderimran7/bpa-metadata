from django.contrib import admin
from common.models import *

admin.site.register(Contact)
admin.site.register(Facility)
admin.site.register(BPA_ID)

class AffiliationAdmin(admin.ModelAdmin):
    fields = (('name', 'description'), )
    list_display = ('name', 'description')

admin.site.register(Affiliation, AffiliationAdmin)
    
    
    

