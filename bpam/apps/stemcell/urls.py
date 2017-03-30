from django.conf.urls import patterns, url

from bpam.decorators import DEBUG_ONLY_VIEW
from . import views

urlpatterns = patterns(
    '',
    url(r'^$', DEBUG_ONLY_VIEW(views.StemCellView.as_view()), name='index'),
    url(r'^sample/(?P<resource_type>[\w-]+)/(?P<pk>.*)/?$', views.SampleDetailView.as_view(), name='sample'),

    url(r'^ckan_refresh/?$', views.CKANRefresh.as_view(), name='ckan_refresh'),
    url(r'^overview/?$', views.ProjectOverviewView.as_view(), name='project_overview'),
)
