from django.conf.urls import url, include
from rest_framework import routers
import views

router = routers.DefaultRouter()
router.register(r"sepsis_samples", views.SepsisSampleViewSet)
router.register(r"hosts", views.HostViewSet)
router.register(r"bpa_ids", views.BPAIDViewSet)
router.register(r"project", views.BPAProjectViewSet)

urlpatterns = [
    url(r'^api/v1/', include(router.urls, namespace="api_v1")),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
