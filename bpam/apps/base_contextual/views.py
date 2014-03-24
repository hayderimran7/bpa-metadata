from django.views.generic import ListView

from .models import ChemicalAnalysis


class ChemicalAnalysisListView(ListView):
    model = ChemicalAnalysis
    context_object_name = 'reports'
