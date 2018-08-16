from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from modeling import views

urlpatterns = [
    url(r'^systems/$', views.system_list, name='system-list'),
    url(r'^systems/(?P<system_id>[0-9]+)/$', views.system_detail, name='system-detail'),
    url(r'^systems/(?P<system_id>[0-9]+)/datasets/$', views.dataset_list, name='dataset-list'),
    url(r'^datasets/(?P<dataset_id>[0-9]+)/$', views.dataset_detail, name='dataset-detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)