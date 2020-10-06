from django.test import TestCase

from ..widgets import NatureOLWidget


class MockNatureOLWidget(NatureOLWidget):
    default_x = 111
    default_y = 222
    default_zoom = 5


class TestNatureOLWidget(TestCase):
    def test_required_attributes_are_set(self):
        widget = MockNatureOLWidget()
        expected_attr_subset = {
            "default_x": 111,
            "default_y": 222,
            "default_zoom": 5,
        }
        self.assertGreater(widget.attrs.items(), expected_attr_subset.items())

    def test_init_can_override_default_attrs(self):
        attrs = {
            "default_x": 888,
            "default_y": 999,
            "default_zoom": 7,
        }
        widget = MockNatureOLWidget(attrs)
        self.assertGreater(widget.attrs.items(), attrs.items())
