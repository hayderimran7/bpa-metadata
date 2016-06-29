from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
                       url(regex=r'^$', view=views.StemCellView.as_view(),
                           name='index'),
                       url(regex=r'^contacts$', view=views.ContactsView.as_view(),
                           name='contacts'), )
