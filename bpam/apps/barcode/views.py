# -*- coding: utf-8 -*-

from django.views.generic import TemplateView, ListView, DetailView

from .models import Sheet

# portal page
class BarcodeView(TemplateView):
    template_name = 'barcode/index.html'

    def get_context_data(self, **kwargs):
        context = super(BarcodeView, self).get_context_data(**kwargs)
        context['sheet_count'] = Sheet.objects.count()
        return context


class SheetListView(ListView):
    model = Sheet
    context_object_name = 'sheets'
    template_name = 'barcode/sheet_list.html'

class SheetDetailView(DetailView):
    model = Sheet
    context_object_name = 'sheet'
    template_name = 'barcode/sheet_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SheetDetailView, self).get_context_data(**kwargs)
        context['sheet'] = Sheet.objects.filter(sheet_number=context['sheet'].sheet_number)

        return context

class ContactsView(TemplateView):
    template_name = 'barcode/contacts.html'
