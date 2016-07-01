# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from apps.common.admin import SampleSiteResource
from apps.common.admin import SampleSiteAdmin

from ..models import MMSite


class MMSiteResource(SampleSiteResource):
    class Meta(SampleSiteResource.Meta):
        model = MMSite


class SiteForm(forms.ModelForm):
    class Meta:
        fields = "__all__"
        model = MMSite
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input-medium',
                                           'style': 'width:50%'}),
            'note': forms.TextInput(attrs={'class': 'input-large',
                                           'style': 'width:50%'})
        }


class MMSiteAdmin(SampleSiteAdmin):
    resource_class = MMSiteResource
    form = SiteForm


admin.site.register(MMSite, MMSiteAdmin)
