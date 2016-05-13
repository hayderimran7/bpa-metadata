# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from suit.widgets import LinkedSelect, AutosizedTextarea, SuitDateWidget, EnclosedInput
from apps.common.admin import SequenceFileAdmin

from .models import (
    Host,
    GenomicsMethod,
    GenomicsFile,
    ProteomicsMethod,
    ProteomicsFile,
    TranscriptomicsMethod,
    TranscriptomicsFile,
    SepsisSample,
)

admin.site.register(Host)
admin.site.register(SepsisSample)
admin.site.register(GenomicsMethod)
admin.site.register(GenomicsFile)
admin.site.register(ProteomicsMethod)
admin.site.register(ProteomicsFile)
admin.site.register(TranscriptomicsMethod)
admin.site.register(TranscriptomicsFile)
