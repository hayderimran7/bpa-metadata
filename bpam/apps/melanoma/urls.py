
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^melanoma/', 'apps.melanoma.views.melanoma_list')
)

