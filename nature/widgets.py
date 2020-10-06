from django.contrib.gis.forms.widgets import OpenLayersWidget
from django.conf import settings


class NatureOLWidget(OpenLayersWidget):
    template_name = "nature/openlayers-nature.html"
    map_width = 800
    map_height = 600
    default_x = 25496615.87
    default_y = 6672343.32
    default_zoom = 12
    map_srid = settings.SRID

    class Media:
        extend = False
        css = {
            "all": (
                "https://cdnjs.cloudflare.com/ajax/libs/ol3/4.6.5/ol.css",
                "https://cdn.jsdelivr.net/npm/ol-layerswitcher@2.0.0/src/ol-layerswitcher.min.css",
                "gis/css/ol3.css",
                "nature/css/nature-ol.css",
            )
        }
        js = (
            "https://cdnjs.cloudflare.com/ajax/libs/ol3/4.6.5/ol.js",
            "https://cdn.jsdelivr.net/npm/ol-layerswitcher@2.0.0/dist/ol-layerswitcher.min.js",
            "nature/js/NatureOLMapWidget.js",
        )

    def __init__(self, attrs=None):
        super().__init__()
        for key in ("default_x", "default_y", "default_zoom"):
            self.attrs[key] = getattr(self, key)
        if attrs:
            self.attrs.update(attrs)
