from django.conf.urls import patterns, url

from bpam.decorators import DEBUG_ONLY_VIEW
from . import views

urlpatterns = patterns(
    '',
    url(r'^$', DEBUG_ONLY_VIEW(views.StemCellView.as_view()), name='index'),
    url(r'^sample/(?P<pk>.*)/$', views.SampleDetailView.as_view(), name='sample'),

    url(r'^overview/$', views.ProjectOverviewView.as_view(), name='project_overview'),
)
