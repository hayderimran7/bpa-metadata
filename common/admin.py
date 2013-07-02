from django.contrib import admin
from common.models import *

admin.site.register(Contact)
admin.site.register(Facility)
admin.site.register(BPA_ID)
admin.site.register(Species)

class AffiliationAdmin(admin.ModelAdmin):
    fields = (('name', 'description'), )
    list_display = ('name', 'description')

admin.site.register(Affiliation, AffiliationAdmin)
    
    
    

