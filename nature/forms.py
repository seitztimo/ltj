from django import forms
from ckeditor.widgets import CKEditorWidget

from nature.models import FeatureClass


class FeatureForm(forms.ModelForm):
    feature_class = forms.ModelChoiceField(
        queryset=FeatureClass.objects.order_by('name'),
        label=FeatureClass._meta.verbose_name.capitalize(),
    )

    class Meta:
        widgets = {
            'text': CKEditorWidget,
            'text_www': CKEditorWidget,
            'description': forms.Textarea,
            'notes': forms.Textarea,
            'name': forms.TextInput(attrs={'size': '80'})
        }


class HabitatTypeObservationInlineForm(forms.ModelForm):

    class Meta:
        widgets = {
            'additional_info': forms.Textarea(attrs={'rows': '5'}),
        }
