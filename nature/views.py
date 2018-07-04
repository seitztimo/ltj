from django.views.generic import DetailView

from .models import Feature


class FeatureReportView(DetailView):
    queryset = Feature.objects.open_data()
    template_name = 'nature/feature-report.html'
