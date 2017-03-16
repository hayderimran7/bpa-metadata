from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import RedirectView, TemplateView

from views import LandingView, GoToCKANView
from apps.common.models import CKANServer

from .decorators import DEBUG_ONLY_VIEW


admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^$', DEBUG_ONLY_VIEW(LandingView.as_view()), name='landing_page'),

    # BASE
    url(r'^base/', include('apps.base.urls', namespace='base')),
    url(r'^base/metagenomics/',
        include('apps.base_metagenomics.urls', namespace='base_metagenomics')),
    url(r'^base/contextual/', include('apps.base_contextual.urls',
                                      namespace='base_contextual')),
    url(r'^base/amplicon/', include('apps.base_amplicon.urls', namespace='base_amplicon')),
    url(r'^base/454/', include('apps.base_454.urls', namespace='base_454')),
    url(r'^base/vocabulary/', include('apps.base_vocabulary.urls',
                                      namespace='base_vocabulary')),
    #  Marine Microbes
    url(r'^marine_microbes/',
        include('apps.marine_microbes.urls', namespace='marine_microbes')),
    # Great Barrier reef
    url(r'^gbr/', include('apps.gbr.urls', namespace='gbr')),
    url(r'^gbr/amplicon/', include('apps.gbr_amplicon.urls', namespace='gbr_amplicon')),
    # Wheat
    url(r'^wheat_cultivars/',
        include('apps.wheat_cultivars.urls', namespace='wheat_cultivars')),
    url(r'^wheat_pathogens/', include('apps.wheat_pathogens.urls',
                                      namespace='wheat_pathogens')),
    url(r'^wheat_pathogens_transcript/',
        include('apps.wheat_pathogens_transcript.urls',
                namespace='wheat_pathogens_transcript')),
    # Melanoma
    url(r'^melanoma/', include('apps.melanoma.urls', namespace='melanoma')),
    # Barcode
    url(r'^barcode/', include('apps.barcode.urls', namespace='barcode')),
    url(r'^stemcell/', include('apps.stemcell.urls', namespace='stemcell')),
    # Sepsis
    url(r'^antibiotic_resistant_pathogens/', include('apps.sepsis.urls', namespace='sepsis')),
    # System
    ('^accounts/', include('django.contrib.auth.urls')),
    url(r'^admin/doc/?', include('django.contrib.admindocs.urls')),
    url(r'^admin/?', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),
    # url(r'^$', TemplateView.as_view(template_name='landing/index.html'), name='landing_page'),
    url(r'^explorer/', include('explorer.urls')),

    url(r'^ckan/', include('bpam.ckan_urls', namespace='ckan')),

    # for anything else redirect to main CKAN site
    url(r'.*', GoToCKANView.as_view(), name='go_to_ckan'),
)


# pattern for serving statically
urlpatterns += patterns('', (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root':
                                                                                     settings.STATIC_ROOT,
                                                                                     'show_indexes': True}))
