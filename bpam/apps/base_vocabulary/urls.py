from django.conf.urls.default import patterns, url

from base_vocabulary import views

urlpatterns = patterns(
    "",
    url(
        regex=r'^api/$',
        view=views.LandUseCreateReadView.as_view(),
        name='landuse_rest_api'
    )
)
