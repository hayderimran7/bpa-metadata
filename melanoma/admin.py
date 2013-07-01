from django.contrib import admin
from melanoma.models import *

admin.site.register(Sample)
admin.site.register(Facility)
admin.site.register(Contact)
admin.site.register(Affiliation)
admin.site.register(DNASource)
admin.site.register(LibraryProtocol)
admin.site.register(Library)
admin.site.register(Array)
admin.site.register(BPA_ID)
admin.site.register(TumorStage)
admin.site.register(Sequencer)

