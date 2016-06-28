from django.views.generic import ListView, DetailView, TemplateView

from apps.common.models import BPAMirror
from .models import (AmpliconSequencingMetadata, AmpliconSequenceFile)


class IndexView(TemplateView):
    template_name = 'gbr_amplicon/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['16S_size'] = AmpliconSequencingMetadata.objects.filter(target='16S').count()
        context['18S_size'] = AmpliconSequencingMetadata.objects.filter(target='18S').count()
        context['ITS_size'] = AmpliconSequencingMetadata.objects.filter(target='ITS').count()
        context['A16S_size'] = AmpliconSequencingMetadata.objects.filter(target='A16S').count()
        context['all_size'] = AmpliconSequencingMetadata.objects.count()
        return context


class AmpliconListView(ListView):
    model = AmpliconSequencingMetadata
    context_object_name = 'metadata_list'
    template_name = 'gbr_amplicon/metadata_list.html'

    def get_context_data(self, **kwargs):
        context = super(AmpliconListView, self).get_context_data(**kwargs)
        context['target'] = 'all'
        context['metadata_list'] = AmpliconSequencingMetadata.objects.select_related('bpa_id', 'sequencing_facility')
        return context


class Amplicon16SListView(AmpliconListView):
    def get_context_data(self, **kwargs):
        context = super(Amplicon16SListView, self).get_context_data(**kwargs)
        context['target'] = '16S'
        context['metadata_list'] = AmpliconSequencingMetadata.objects.filter(target='16S').select_related(
            'bpa_id', 'sequencing_facility')
        return context


class Amplicon18SListView(AmpliconListView):
    def get_context_data(self, **kwargs):
        context = super(Amplicon18SListView, self).get_context_data(**kwargs)
        context['target'] = '18S'
        context['metadata_list'] = AmpliconSequencingMetadata.objects.filter(target='18S').select_related(
            'bpa_id', 'sequencing_facility')
        return context


class AmpliconITSListView(AmpliconListView):
    def get_context_data(self, **kwargs):
        context = super(AmpliconITSListView, self).get_context_data(**kwargs)
        context['target'] = 'ITS'
        context['metadata_list'] = AmpliconSequencingMetadata.objects.filter(target='ITS').select_related(
            'bpa_id', 'sequencing_facility')
        return context


class AmpliconA16SListView(AmpliconListView):
    def get_context_data(self, **kwargs):
        context = super(AmpliconA16SListView, self).get_context_data(**kwargs)
        context['target'] = 'A16S'
        context['metadata_list'] = AmpliconSequencingMetadata.objects.filter(target='A16S').select_related(
            'bpa_id', 'sequencing_facility')
        return context


class AmpliconDetailView(DetailView):
    model = AmpliconSequencingMetadata
    context_object_name = 'metadata'
    template_name = 'gbr_amplicon/metadata_detail.html'

    def get_context_data(self, **kwargs):
        context = super(AmpliconDetailView, self).get_context_data(**kwargs)
        context['sequencefiles'] = AmpliconSequenceFile.objects.filter(sample__bpa_id=context['metadata'].bpa_id)
        context['sample'] = context['metadata']  # same name to make common sequence file template work
        context['mirrors'] = BPAMirror.objects.all()
        return context
