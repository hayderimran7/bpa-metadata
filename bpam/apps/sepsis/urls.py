from django.conf.urls import url, include
from rest_framework import routers
import views

router = routers.DefaultRouter()
router.register(r"sepsis_samples", views.SepsisSampleViewSet)
router.register(r"hosts", views.HostViewSet)
router.register(r"project", views.BPAProjectViewSet)
router.register(r"bpa_ids", views.BPAIDViewSet)
router.register(r"track_genomics", views.GenomicsMiseqFileViewSet)
router.register(r"genomic_miseq_files", views.GenomicsMiseqFileViewSet)
router.register(r"genomic_pacbio_files", views.GenomicsPacBioFileViewSet)

router.register(r"track_pacbio", views.PacBioTrackViewSet)
router.register(r"track_miseq", views.MiSeqTrackViewSet)
router.register(r"track_rna_hiseq", views.RNAHiSeqTrackViewSet)
router.register(r"track_metabolomics", views.MetabolomicsTrackViewSet)
router.register(r"track_deeplc", views.DeepLCMSTrackViewSet)
router.register(r"track_swath", views.SWATHMSTrackViewSet)

urlpatterns = [
    url(r'^api/v2/', include(router.urls)),
    url(regex=r'^$', view=views.SepsisView.as_view(), name='index'),
    url(regex=r'^contacts$', view=views.ContactsView.as_view(),
        name='contacts'),
    url(regex=r'^samples', view=views.SampleListView.as_view(),
        name='samples'),
    url(regex=r'^sample/(?P<pk>.*)/$',
        view=views.SampleDetailView.as_view(),
        name='sample'),
    url(regex=r'^sampletracks', view=views.TrackListView.as_view(),
        name='sampletracks'),
    url(regex=r'^genomicsmiseqfiles',
        view=views.GenomicsMiseqFileListView.as_view(),
        name='genomics_miseq_files'),
    url(regex=r'^transcriptomicshiseqfiles',
        view=views.TranscriptomicsHiseqFileListView.as_view(),
        name='transcriptomics_hiseq_files'),
    url(regex=r'^genomicspacbiofiles',
        view=views.GenomicsPacBioFileListView.as_view(),
        name='genomics_pacbio_files'),
    url(regex=r'^consortium$', view=views.ConsortiumView.as_view(),
        name='consortium'),

    # BEGIN----- Tracker URLs ----------

    url(regex=r'^overview/$',
        view=views.TrackOverview.as_view(),
        name='overview'),

    url(regex=r'^overview/data/$',
        view=views.TrackOverviewConstraints.as_view(),
        name='overview_constraints'),

    url(regex=r'^overview/(?P<constraint>.*)/(?P<status>.*)/$',
        view=views.TrackDetails.as_view(),
        name='overview_detail'),

    # END------- Tracker URLs ----------
]
