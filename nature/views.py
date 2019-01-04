import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views import View

from .models import Feature, Species, ObservationSeries, Observation
from .utils import signature_is_valid


class ProtectedReportViewMixin:
    """
    A report view mixin class that allows staff users
    to access all reports, but only open data for
    non-staff users
    """

    def __init__(self):
        self.groups = None

    def get(self, request, pk):
        if 'HTTP_SIGNATURE' and 'HTTP_DATE' and 'HTTP_HOST' and 'HTTP_X_FORWARDED_GROUPS' in request.META:
            received_signature = request.META['HTTP_SIGNATURE']
            date = request.META['HTTP_DATE']
            host = request.META['HTTP_HOST']
            groups_string = request.META['HTTP_X_FORWARDED_GROUPS']
            request_line = '{0} {1} {2}'.format(request.META['REQUEST_METHOD'], request.get_full_path(), 'HTTP/1.1')
            if signature_is_valid(date, host, groups_string, request_line, received_signature):
                self.groups = groups_string.split(';')
            else:
                raise Http404
        return super().get(request)

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_staff:
            return qs
        if self.groups:
            if 'ltj_admin' in self.groups or r'HELS000627\Paikkatietovipunen_ltj_admin' in self.groups:
                return qs.for_admin()
            elif 'ltj_virka_hki' in self.groups or r'HELS000627\Paikkatietovipunen_ltj_virka' in self.groups:
                return qs.for_office_hki()
            elif 'ltj_virka' in self.groups:
                return qs.for_office()
        return qs.www()


class FeatureReportView(ProtectedReportViewMixin, DetailView):
    queryset = Feature.objects.all()
    template_name = 'nature/reports/feature-report.html'


class ObservationReportView(ProtectedReportViewMixin, DetailView):
    queryset = Observation.objects.all()
    template_name = 'nature/reports/observation-report.html'


class SpeciesReportView(ProtectedReportViewMixin, DetailView):
    queryset = Species.objects.all()
    template_name = 'nature/reports/species-report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context['observations'] = self.get_ordered_observations()
        return context

    def get_ordered_observations(self):
        if self.request.user.is_staff:
            queryset = self.object.observations.all()
        else:
            queryset = self.object.observations.open_data()
        return queryset.select_related('feature__feature_class').order_by('feature__feature_class__name')


class SpeciesRegulationsReportView(ProtectedReportViewMixin, DetailView):
    queryset = Species.objects.all()
    template_name = 'nature/reports/species-regulations-report.html'


class ObservationSeriesReportView(DetailView):
    queryset = ObservationSeries.objects.all()
    template_name = 'nature/reports/observationseries-report.html'


class FeatureObservationsReportView(ProtectedReportViewMixin, DetailView):
    queryset = Feature.objects.all()
    template_name = 'nature/reports/feature-observations-report.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.object:
            context_data['feature_observations'] = self.object.observations.all().order_by('species__name_fi')
        return context_data


class FeatureHabitatTypeObservationsReportView(ProtectedReportViewMixin, DetailView):
    queryset = Feature.objects.all()
    template_name = 'nature/reports/feature-habitattypeobservations-report.html'


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
