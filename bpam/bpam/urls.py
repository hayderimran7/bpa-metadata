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
    url(r'^base/?', include('apps.base.urls', namespace='base')),
    url(r'^base/metagenomics/', include('apps.base_metagenomics.urls', namespace='basemetagenomics')),
    url(r'^base/contextual/', include('apps.base_contextual.urls', namespace='basecontextual')),
    url(r'^gbr/?', include('apps.gbr.urls', namespace='gbr')),
    url(r'^wheat_cultivars/?', include('apps.wheat_cultivars.urls', namespace='wheat_cultivars')),
    url(r'^wheat_pathogens/?', include('apps.wheat_pathogens.urls', namespace='wheat_pathogens')),
    url(r'^melanoma/', include('apps.melanoma.urls', namespace='melanoma')),
    ('^accounts/', include('django.contrib.auth.urls')),
    (r'^api/', include(v1_api.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r"^$", TemplateView.as_view(template_name="landing/index.html"), name='landing-page'),
    url(r'^explorer/', include('explorer.urls')),
)
