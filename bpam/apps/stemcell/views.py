# -*- coding: utf-8 -*-

from django.views.generic import TemplateView


class StemCellView(TemplateView):
    template_name = 'stemcell/index.html'


class ContactsView(TemplateView):
    template_name = 'stemcell/contacts.html'
