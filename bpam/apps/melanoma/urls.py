
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required, permission_required

from apps.melanoma.views import MelanomaSequenceFileListView

urlpatterns = patterns('',
    url(r'^melanoma/', login_required(MelanomaSequenceFileListView.as_view()), name="melanoma-list"),
)
