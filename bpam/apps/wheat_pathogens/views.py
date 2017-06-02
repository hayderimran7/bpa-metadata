from apps.common.views import DebugOnlyTemplateView
from bpam.views import CKANTemplateView


class IndexView(DebugOnlyTemplateView):
    template_name = 'wheat_pathogens/index.html'


class SampleListView(CKANTemplateView):
    template_name = 'wheat_pathogens/sample_list.html'


class SequenceFileListView(CKANTemplateView):
    template_name = 'wheat_pathogens/sequencefile_list.html'
