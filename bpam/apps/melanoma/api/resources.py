from tastypie.resources import ModelResource
from apps.melanoma.models import MelanomaSequenceFile
from tastypie.authentication import SessionAuthentication

class MelanomaSequenceFileResource(ModelResource):
    class Meta:
        queryset = MelanomaSequenceFile.objects.all()
        allowed_methods = ['get']
        authentication = SessionAuthentication()
        limit = 10000
        max_limit = None
