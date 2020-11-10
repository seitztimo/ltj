import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView

from nature.hmac import HMACAuth
from .enums import UserRole
from .models import Feature, Species, ObservationSeries, Observation


class ProtectedReportViewMixin:
    """View mixin for protected reports

    Allow accessing all reports for staff users and public reports
    for non-staff users. If the requests is a hmac request, the
    reports are filtered based on forwarded authorization groups.
    """

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_staff:
            return qs

        hmac_auth = self._get_hmac_auth()
        role = hmac_auth.user_role
        if role == UserRole.ADMIN:
            return qs.for_admin()
        elif role == UserRole.OFFICE_HKI:
            return qs.for_office_hki()
        elif role == UserRole.OFFICE:
            return qs.for_office()

        return qs.www()

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        admin_hmac_roles = [UserRole.ADMIN, UserRole.OFFICE_HKI, UserRole.OFFICE]
        hmac_auth = self._get_hmac_auth()
        user_role = (
            UserRole.ADMIN if self.request.user.is_staff else hmac_auth.user_role
        )
        user_is_in_admin_groups = (
            self.request.user.is_staff or hmac_auth.user_role in admin_hmac_roles
        )
        context_data["user_role"] = user_role.value
        context_data["user_is_in_admin_groups"] = user_is_in_admin_groups

        return context_data

    def _get_hmac_auth(self):
        if not hasattr(self, "_hmac_auth"):
            self._hmac_auth = HMACAuth(self.request)
        return self._hmac_auth


class ProtectedObservationListReportViewMixin(ProtectedReportViewMixin):
    """View mixin to filter observations based on user roles"""

    def get_observation_queryset(self):
        raise NotImplementedError

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.object:
            context_data["observations"] = self.get_filtered_observations()
            context_data[
                "secret_observation_count"
            ] = self.get_secret_observation_count()
        return context_data

    def get_filtered_observations(self):
        """Get filtered observations based on hmac user roles"""
        qs = self.get_observation_queryset()
        hmac_auth = self._get_hmac_auth()
        role = hmac_auth.user_role
        if self.request.user.is_staff or role == UserRole.ADMIN:
            qs = qs.for_admin()
        elif role == UserRole.OFFICE_HKI:
            qs = qs.for_office_hki()
        elif role == UserRole.OFFICE:
            qs = qs.for_office()
        else:
            qs = qs.www()
        return qs

    def get_secret_observation_count(self):
        """Return the number of secret observations for current user role"""
        hmac_auth = self._get_hmac_auth()
        user_role = hmac_auth.user_role

        if user_role not in [UserRole.OFFICE_HKI, user_role.OFFICE]:
            return 0

        qs = self.get_observation_queryset()
        admin_qs = qs.for_admin()
        office_qs = (
            qs.for_office_hki() if user_role == UserRole.OFFICE_HKI else qs.for_office()
        )

        return admin_qs.difference(office_qs).count()


class ValidRegulationsViewMixin(ProtectedReportViewMixin):
    def get_regulations_queryset(self):
        raise NotImplementedError

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.object:
            context_data["regulations"] = self.get_filtered_regulations()
        return context_data

    def get_filtered_regulations(self):
        qs = self.get_regulations_queryset().exclude(valid=False)
        return qs


class FeatureReportView(
    ProtectedObservationListReportViewMixin, ProtectedReportViewMixin, DetailView
):
    queryset = Feature.objects.all()
    template_name = "nature/reports/feature-report.html"

    def get_observation_queryset(self):
        return self.object.observations.all()

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.object:
            context_data[
                "transactions"
            ] = self.object.transactions.all().prefetch_related("regulations")
        return context_data


class ObservationReportView(ProtectedReportViewMixin, DetailView):
    queryset = Observation.objects.all()
    template_name = "nature/reports/observation-report.html"


class SpeciesReportView(
    ProtectedObservationListReportViewMixin, ValidRegulationsViewMixin, DetailView
):
    queryset = Species.objects.all()
    template_name = "nature/reports/species-report.html"

    def get_observation_queryset(self):
        return self.object.observations.all().order_by("feature__feature_class__name")

    def get_regulations_queryset(self):
        return self.object.regulations.all()


class SpeciesRegulationsReportView(ValidRegulationsViewMixin, DetailView):
    model = Species
    template_name = "nature/reports/species-regulations-report.html"

    def get_regulations_queryset(self):
        return self.object.regulations.all()


class ObservationSeriesReportView(DetailView):
    queryset = ObservationSeries.objects.all()
    template_name = "nature/reports/observationseries-report.html"


class FeatureObservationsReportView(
    ProtectedObservationListReportViewMixin, DetailView
):
    queryset = Feature.objects.all()
    template_name = "nature/reports/feature-observations-report.html"

    def get_observation_queryset(self):
        return self.object.observations.all().order_by("species__name_fi")


class FeatureHabitatTypeObservationsReportView(ProtectedReportViewMixin, DetailView):
    queryset = Feature.objects.all()
    template_name = "nature/reports/feature-habitattypeobservations-report.html"


@method_decorator(login_required, name="dispatch")
class FeatureWFSView(View):
    def get(self, request, *args, **kwargs):
        url = self._get_wfs_url()
        r = requests.get(url)
        return HttpResponse(
            content=r.content,
            content_type=r.headers["content-type"],
            status=r.status_code,
        )

    def _get_wfs_url(self):
        query_dict = self.request.GET.copy()
        query_dict.setlist("typeName", [self._get_layer_typename()])
        return "{0}?{1}".format(settings.WFS_SERVER_URL, query_dict.urlencode())

    def _get_layer_typename(self):
        return "{0}:{1}".format(
            settings.WFS_NAMESPACE, self.request.GET.get("typeName")
        )
