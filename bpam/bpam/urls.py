from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

from apps.melanoma.api.resources import MelanomaSequenceFileResource
from django.views.generic import TemplateView

from tastypie.api import Api

v1_api = Api(api_name='v1')
v1_api.register(MelanomaSequenceFileResource())

urlpatterns = patterns(
    '',
    url(r'^base$', include('apps.base.urls')),
    url(r'^base/metagenomics/', include('apps.base_metagenomics.urls')),
    url(r'^base/contextual/', include('apps.base_contextual.urls')),
    url(r'^melanoma/', include('apps.melanoma.urls')),
    ('^accounts/', include('django.contrib.auth.urls')),
    (r'^api/', include(v1_api.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r"^$", TemplateView.as_view(template_name="landing/index.html"), name='landing-page'),
    url(r'^explorer/', include('explorer.urls')),
)
