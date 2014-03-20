from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',
    url(
        regex=r'^$',
        view=views.MelanomaSequenceFileListView.as_view(),
        name='sequencefiles'),
    # url(
    #     r'^all$',
    #     login_required(MelanomaSequenceFileListView.as_view()),
    #     name="all"),
    # url(
    #     r'search/(.*)$',
    #     login_required(search_view),
    #     name="search"),
)
