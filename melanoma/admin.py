from django.contrib import admin
from melanoma.models import *

admin.site.register(Sample)


admin.site.register(DNASource)
admin.site.register(LibraryProtocol)
admin.site.register(Library)
admin.site.register(Array)

admin.site.register(TumorStage)
admin.site.register(Sequencer)

