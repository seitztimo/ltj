from django.contrib.gis.forms.widgets import OSMWidget
from django.conf import settings


class NatureOLWidget(OSMWidget):
    template_name = 'nature/openlayers-nature.html'
    map_srid = settings.SRID

    default_lon = 25496731.185709
    default_lat = 6672620.498890

    class Media:
        extend = False
        css = {
            'all': (
                'https://cdnjs.cloudflare.com/ajax/libs/ol3/4.6.5/ol.css',
                'gis/css/ol3.css',
            )
        }
        js = (
            'https://cdnjs.cloudflare.com/ajax/libs/ol3/4.6.5/ol.js',
            'nature/js/NatureOLMapWidget.js',
        )
