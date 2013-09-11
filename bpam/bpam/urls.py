from django.conf.urls import patterns, include, url
import django.contrib.auth
from django.contrib import admin
admin.autodiscover()

from apps.melanoma.api.resources import MelanomaSequenceFileResource

from tastypie.api import Api
v1_api = Api(api_name='v1')
v1_api.register(MelanomaSequenceFileResource())


urlpatterns = patterns('',
    url(r'', include('apps.common.urls')),
    url(r'', include('apps.melanoma.urls')),
    ('^accounts/', include('django.contrib.auth.urls')),
    (r'^api/', include(v1_api.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^qbe/', include('django_qbe.urls')),
)
