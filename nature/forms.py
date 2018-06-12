from django import forms
from ckeditor.widgets import CKEditorWidget

from nature.models import FeatureClass


class FeatureForm(forms.ModelForm):
    feature_class = forms.ModelChoiceField(queryset=FeatureClass.objects.order_by('name'))

    class Meta:
        widgets = {
            'text': CKEditorWidget,
            'text_www': CKEditorWidget,
        }
