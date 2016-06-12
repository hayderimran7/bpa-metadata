from django.views.generic import TemplateView

from apps.melanoma.models import MelanomaSample
from apps.sepsis.models import SepsisSample
from apps.gbr.models import GBRSample
from apps.base.models import BASESample
from apps.wheat_cultivars.models import CultivarSample
from apps.wheat_pathogens.models import PathogenSample as WheatPathogenSample
from apps.wheat_pathogens_transcript.models import WheatPathogenTranscriptSample


class LandingView(TemplateView):
    template_name = 'landing/index.html'

    def get_context_data(self, **kwargs):
        context = super(LandingView, self).get_context_data(**kwargs)
        context['melanoma_sample_count'] = MelanomaSample.objects.count()
        context['sepsis_sample_count'] = SepsisSample.objects.count()
        context['gbr_sample_count'] = GBRSample.objects.count()
        context['base_sample_count'] = BASESample.objects.count()
        context['wheat_cultivars_sample_count'] = CultivarSample.objects.count()
        context['wheat_pathogens_genome_sample_count'] = WheatPathogenSample.objects.count()
        context['wheat_pathogens_transcript_sample_count'] = WheatPathogenTranscriptSample.objects.count()

        return context
