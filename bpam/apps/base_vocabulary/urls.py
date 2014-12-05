from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    "",
    url(
        regex=r'^landuse/$',
        view=views.LandUseCreateReadView.as_view(),
        name='landuse_rest_api'
    ),
    url(
        regex=r'^soiltexture/$',
        view=views.SoilTextureCreateReadView.as_view(),
        name='soiltexture_rest_api'
    ),
    url(
        regex=r'^soilcolour/$',
        view=views.SoilColourCreateReadView.as_view(),
        name='soilcolour_rest_api'
    )
)
