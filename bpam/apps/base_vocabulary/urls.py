from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    "",
    url(
        regex=r'^api/$',
        view=views.LandUseCreateReadView.as_view(),
        name='landuse_rest_api'
    )
)
