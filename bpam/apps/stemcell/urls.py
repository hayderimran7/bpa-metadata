from django.conf.urls import patterns, url

from bpam.decorators import DEBUG_ONLY_VIEW
from bpam.views import CKANTemplateView
from . import views

urlpatterns = patterns(
    '',
    url(r'^$', DEBUG_ONLY_VIEW(views.StemCellView.as_view()), name='index'),

    url(r'^ckan_refresh/?$', views.CKANRefresh.as_view(), name='ckan_refresh'),
    url(r'^overview/?$',
        CKANTemplateView.as_view(template_name='stemcell/project_overview.html'),
        name='project_overview'),
)
