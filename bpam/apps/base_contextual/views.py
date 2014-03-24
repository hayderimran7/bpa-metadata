from django.views.generic import ListView

from .models import ChemicalAnalysis


class ChemicalAnalysisListView(ListView):
    model = ChemicalAnalysis
