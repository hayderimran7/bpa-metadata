from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    "",
    url(
        regex=r'^vocabularies/$',
        view=views.VocabularyView.as_view(),
        name='all_vocabularies'
    ),
    url(
        regex=r'^landuse/$',
        view=views.LandUseReadView.as_view(),
        name='landuse_rest_api'
    ),
    url(
        regex=r'^soiltexture/$',
        view=views.SoilTextureReadView.as_view(),
        name='soiltexture_rest_api'
    ),
    url(
        regex=r'^soilcolour/$',
        view=views.SoilColourReadView.as_view(),
        name='soilcolour_rest_api'
    ),
    url(
        regex=r'^generalecologicalzone/$',
        view=views.GeneralEcologicalZoneReadView.as_view(),
        name='generalecologicalzone_rest_api'
    ),
    url(
        regex=r'^broadvegetationtype/$',
        view=views.BroadVegetationTypeView.as_view(),
        name='broadvegetationtype_rest_api'
    ),
    url(
        regex=r'^tillagetype/$',
        view=views.TillageTypeReadView.as_view(),
        name='tillagetype_rest_api'
    ),
    url(
        regex=r'^horizonclassification/$',
        view=views.HorizonClassificationReadView.as_view(),
        name='horizonclassification_rest_api'
    ),
    url(
        regex=r'^australiansoilclassification/$',
        view=views.AustralianSoilClassificationReadView.as_view(),
        name='australiansoilclassification_rest_api'
    ),
    url(
        regex=r'^faosoilclassification/$',
        view=views.FAOSoilClassificationReadView.as_view(),
        name='faosoilclassification_rest_api'
    ),
    url(
        regex=r'^drainageclassification/$',
        view=views.DrainageClassificationReadView.as_view(),
        name='drainageclassification_rest_api'
    ),
    url(
        regex=r'^profileposition/$',
        view=views.ProfilePositionReadView.as_view(),
        name='profileposition_rest_api'
    )
)
