import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views import View

from .models import Feature, Species, ObservationSeries, Observation


class FeatureReportView(DetailView):
    queryset = Feature.objects.open_data()
    template_name = 'nature/feature-report.html'


class ObservationReportView(DetailView):
    queryset = Observation.objects.open_data()
    template_name = 'nature/observation-report.html'


class SpeciesReportView(DetailView):
    queryset = Species.objects.open_data()
    template_name = 'nature/species-report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context['feature_classes'] = {}
            for observation in self.object.observations.all():
                feature_class = observation.feature.feature_class
                if feature_class.id not in context['feature_classes'].keys():
                    context['feature_classes'][feature_class.id] = {
                        'name': feature_class.name,
                        'observations': [],
                    }
                context['feature_classes'][feature_class.id]['observations'].append(observation)
        return context


class ObservationSeriesView(DetailView):
    queryset = ObservationSeries.objects.all()
    template_name = 'nature/observationseries-report.html'


@method_decorator(login_required, name='dispatch')
class FeatureWFSView(View):

    def get(self, request, *args, **kwargs):
        url = self._get_wfs_url()
        r = requests.get(url)
        return HttpResponse(
            content=r.content,
            content_type=r.headers['content-type'],
            status=r.status_code,
        )

    def _get_wfs_url(self):
        query_dict = self.request.GET.copy()
        query_dict.setlist('typeName', [self._get_layer_typename()])
        return '{0}?{1}'.format(settings.WFS_SERVER_URL, query_dict.urlencode())

    def _get_layer_typename(self):
        return '{0}:{1}'.format(settings.WFS_NAMESPACE, self.request.GET.get('typeName'))
