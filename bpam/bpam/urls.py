from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns(
    '',
    # rest api
    url(r'^api/', include('rest_framework.urls', namespace='rest_framework')),
    # BASE
    url(r'^base/', include('apps.base.urls', namespace='base')),
    url(r'^base/metagenomics/', include('apps.base_metagenomics.urls', namespace='base_metagenomics')),
    url(r'^base/contextual/', include('apps.base_contextual.urls', namespace='base_contextual')),
    url(r'^base/amplicon/', include('apps.base_amplicon.urls', namespace='base_amplicon')),
    url(r'^base/454/', include('apps.base_454.urls', namespace='base_454')),
    url(r'^base/vocabulary/', include('apps.base_vocabulary.urls', namespace='base_vocabulary')),
    # Great Barrier reef
    url(r'^gbr/', include('apps.gbr.urls', namespace='gbr')),
    # Wheat
    url(r'^wheat_cultivars/', include('apps.wheat_cultivars.urls', namespace='wheat_cultivars')),
    url(r'^wheat_pathogens/', include('apps.wheat_pathogens.urls', namespace='wheat_pathogens')),
    url(r'^wheat_pathogens_transcript/',
        include('apps.wheat_pathogens_transcript.urls', namespace='wheat_pathogens_transcript')),
    # Melanoma
    url(r'^melanoma/', include('apps.melanoma.urls', namespace='melanoma')),
    # System
    ('^accounts/', include('django.contrib.auth.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^$', TemplateView.as_view(template_name='landing/index.html'), name='landing_page'),
    url(r'^explorer/', include('explorer.urls')),
)

# pattern for serving statically
if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^static/(?P<path>.*)$', 'django.views.static.serve',
                             {'document_root': settings.STATIC_ROOT, 'show_indexes': True}))
