from django.conf.urls import url

from . import views

app_name = 'nature'
urlpatterns = [
    url(r'^feature-report/(?P<pk>\d+)/$', views.FeatureReportView.as_view(), name='feature-report'),
    url(r'^observationseries-report/(?P<pk>\d+)/$', views.ObservationSeriesView.as_view(),
        name='observationseries-report'),
    url(r'^feature-observations-report/(?P<pk>\d+)/$', views.FeatureObservationsView.as_view(),
        name='feature-observations-report'),
    url(r'^feature-habitattypeobservations-report/(?P<pk>\d+)/$', views.FeatureHabitatTypeObservationsView.as_view(),
        name='feature-habitattypeobservations-report'),
    url(r'^species-report/(?P<pk>\d+)/$', views.SpeciesReportView.as_view(), name='species-report'),
    url(r'^species-regulations-report/(?P<pk>\d+)/$', views.SpeciesRegulationsReportView.as_view(),
        name='species-regulations-report'),
    url(r'^observation-report/(?P<pk>\d+)/$', views.ObservationReportView.as_view(), name='observation-report'),
    url(r'^wfs', views.FeatureWFSView.as_view(), name='wfs'),
]
