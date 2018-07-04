from django.conf.urls import url

from . import views

app_name = 'nature'
urlpatterns = [
    url(r'^feature-report/(?P<pk>\d+)/$', views.FeatureReportView.as_view(), name='feature-report'),
]
