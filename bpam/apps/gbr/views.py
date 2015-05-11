from django.views.generic import TemplateView, ListView, DetailView

from .models import GBRSample, GBRSequenceFile, CollectionEvent, CollectionSite


class GBRView(TemplateView):
    template_name = 'gbr/index.html'

    def get_context_data(self, **kwargs):
        context = super(GBRView, self).get_context_data(**kwargs)
        context['sample_count'] = GBRSample.objects.count()
        context['file_count'] = GBRSequenceFile.objects.count()
        context['collection_events_count'] = CollectionEvent.objects.count()
        context['collection_sites_count'] = CollectionSite.objects.count()
        return context


class SampleListView(ListView):
    model = GBRSample
    context_object_name = 'samples'
    template_name = 'gbr/sample_list.html'


class SampleDetailView(DetailView):
    model = GBRSample
    context_object_name = 'sample'
    template_name = 'gbr/sample_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SampleDetailView, self).get_context_data(**kwargs)
        context['sequencefiles'] = GBRSequenceFile.objects.filter(sample__bpa_id=context['sample'].bpa_id)

        return context


class SequenceFileListView(ListView):
    model = GBRSequenceFile
    context_object_name = 'sequencefiles'
    template_name = 'gbr/sequencefile_list.html'


class CollectionEventListView(ListView):
    model = CollectionEvent
    context_object_name = 'collections'
    template_name = 'gbr/collection_event_list.html'
    queryset = CollectionEvent.objects.select_related('site', 'collector')


class CollectionSiteListView(ListView):
    model = CollectionSite
    context_object_name = 'sites'
    template_name = 'gbr/collection_site_list.html'


class CollectionSiteDetailView(DetailView):
    model = CollectionSite
    context_object_name = 'collectionsite'
    template_name = 'gbr/collectionsite_detail.html'


class CollectionView(DetailView):
    model = CollectionEvent
    context_object_name = 'collectionevent'
    template_name = 'gbr/collection_event_detail.html'


class ContactsView(TemplateView):
    template_name = 'gbr/contacts.html'
