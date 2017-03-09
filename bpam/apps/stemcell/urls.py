from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(regex=r'^$', view=views.StemCellView.as_view(),
        name='index'),
    url(regex=r'^contacts$', view=views.ContactsView.as_view(),
        name='contacts'),
    url(regex=r'^sample/(?P<pk>.*)/$',
        view=views.SampleDetailView.as_view(),
        name='sample'),

    url(regex=r'^overview/$',
        view=views.ProjectOverviewView.as_view(),
        name='project_overview'),

#    url(regex=r'^overview/data/$',
#        view=tracker_views.OverviewConstraints.as_view(),
#        name='overview_constraints'),
)
