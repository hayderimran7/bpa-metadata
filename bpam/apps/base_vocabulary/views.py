from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from .models import LandUse

class LandUseCreateReadView(ListCreateAPIView):
    model = LandUse

class LandUseReadUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    model = LandUse