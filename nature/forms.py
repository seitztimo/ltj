from django import forms
from ckeditor.widgets import CKEditorWidget


class FeatureForm(forms.ModelForm):

    class Meta:
        widgets = {
            'text': CKEditorWidget,
            'text_www': CKEditorWidget,
            'description': forms.Textarea,
            'notes': forms.Textarea,
            'name': forms.TextInput(attrs={'size': '80'})
        }
