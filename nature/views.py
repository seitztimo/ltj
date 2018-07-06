import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views import View

from .models import Feature


class FeatureReportView(DetailView):
    queryset = Feature.objects.open_data()
    template_name = 'nature/feature-report.html'


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
