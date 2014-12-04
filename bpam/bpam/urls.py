from django.conf.urls import patterns, include, url
from django.contrib import admin

from apps.melanoma.api.resources import MelanomaSequenceFileResource
from django.views.generic import TemplateView

from tastypie.api import Api
from django.db.models.loading import cache as model_cache

if not model_cache.loaded:
    model_cache.get_models()

v1_api = Api(api_name='v1')
v1_api.register(MelanomaSequenceFileResource())

admin.autodiscover()

urlpatterns = patterns(
    '',
    # rest api
    url(r'^api/', include('rest_framework.urls', namespace='rest_framework')),
    # BASE
    url(r'^base/', include('apps.base.urls', namespace='base')),
    url(r'^base/metagenomics/', include('apps.base_metagenomics.urls', namespace='basemetagenomics')),
    url(r'^base/contextual/', include('apps.base_contextual.urls', namespace='basecontextual')),
    url(r'^base/amplicon/', include('apps.base_amplicon.urls', namespace='base_amplicon')),
    url(r'^base/454/', include('apps.base_454.urls', namespace='base454')),
    # Great Barrier reef
    url(r'^gbr/', include('apps.gbr.urls', namespace='gbr')),
    # Wheat
    url(r'^wheat_cultivars/', include('apps.wheat_cultivars.urls', namespace='wheat_cultivars')),
    url(r'^wheat_pathogens/', include('apps.wheat_pathogens.urls', namespace='wheat_pathogens')),
    url(r'^wheat_pathogens_transcript/', include('apps.wheat_pathogens_transcript.urls', namespace='wheat_pathogens_transcript')),
    # Melanoma
    url(r'^melanoma/', include('apps.melanoma.urls', namespace='melanoma')),
    # System
    ('^accounts/', include('django.contrib.auth.urls')),
    (r'^api/', include(v1_api.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r"^$", TemplateView.as_view(template_name="landing/index.html"), name='landing-page'),
    url(r'^explorer/', include('explorer.urls')),
)

