from django.conf.urls import url, include
from rest_framework import routers
import views

router = routers.DefaultRouter()
router.register(r"sepsis_samples", views.SepsisSampleViewSet)
router.register(r"hosts", views.HostViewSet)
router.register(r"project", views.BPAProjectViewSet)
router.register(r"bpa_ids", views.BPAIDViewSet)
router.register(r"track", views.SepsisSampleTrackViewSet)
router.register(r"proteomic_files", views.ProteomicsFileViewSet)
router.register(r"genomic_files", views.GenomicsFileViewSet)
router.register(r"transcriptomic_files", views.TranscriptomicsFileViewSet)

urlpatterns = [
    url(r'^api/v1/', include(router.urls)),
    url(
        regex=r'^$',
        view=views.SepsisView.as_view(),
        name='index'),
    url(
        regex=r'^contacts$',
        view=views.ContactsView.as_view(),
        name='contacts'),
    url(
        regex=r'^samples',
        view=views.SampleListView.as_view(),
        name='samples'),
    url(
        regex=r'^sample/(?P<pk>.*)/$',
        view=views.SampleDetailView.as_view(),
        name='sample'),
    url(
        regex=r'^genomicsfiles',
        view=views.GenomicsFileListView.as_view(),
        name='genomicsfiles'),
]
