from django import forms
from ckeditor.widgets import CKEditorWidget


class FeatureForm(forms.ModelForm):

    class Meta:
        widgets = {
            'text': CKEditorWidget,
            'text_www': CKEditorWidget,
        }