# -*- coding: utf-8 -*-

from django.views.generic import TemplateView, ListView, DetailView

from .models import Sheet


class BarcodeIndex(TemplateView):
    template_name = "barcode/index.html"


class PilbaraFloraIndex(TemplateView):
    template_name = "barcode/pilbara_plant_diversity.html"

    def get_context_data(self, **kwargs):
        context = super(PilbaraFloraIndex, self).get_context_data(**kwargs)
        context["sheet_count"] = Sheet.objects.count()
        return context


class PilbaraCollectionSiteListView(ListView):
    model = Sheet
    context_object_name = 'sheets'
    template_name = "barcode/pilbara_collection_site_list.html"


class SheetListView(ListView):
    model = Sheet
    context_object_name = "sheets"
    template_name = "barcode/sheet_list.html"


class SheetDetailView(DetailView):
    model = Sheet
    context_object_name = "sheet"
    template_name = "barcode/sheet_detail.html"

    def get_context_data(self, **kwargs):
        context = super(SheetDetailView, self).get_context_data(**kwargs)
        context["sequencefiles"] = []
        return context


class ContactsView(TemplateView):
    template_name = "barcode/contacts.html"
