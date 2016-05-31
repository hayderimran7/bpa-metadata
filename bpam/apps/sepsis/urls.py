from django.conf.urls import url, include
from rest_framework import routers
import views

router = routers.DefaultRouter()
router.register(r"sepsis_samples", views.SepsisSampleViewSet)
router.register(r"hosts", views.HostViewSet)
router.register(r"project", views.BPAProjectViewSet)
router.register(r"bpa_ids", views.BPAIDViewSet)
router.register(r"track", views.SepsisSampleTrackViewSet)
router.register(r"genomic_miseq_files", views.GenomicsMiseqFileViewSet)

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
        regex=r'^genomicsmiseqfiles',
        view=views.GenomicsMiseqFileListView.as_view(),
        name='genomics_miseq_files'),
]
