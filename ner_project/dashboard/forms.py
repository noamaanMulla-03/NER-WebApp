from django import forms
from django.forms.widgets import ClearableFileInput
from .models import DocumentSet

# Custom widget to support multiple file uploads
class MultipleFileInput(ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleFileInput(attrs={'multiple': True}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        if not data:
            return None
        if isinstance(data, (list, tuple)):
            return data
        return [data]

class DocumentUploadForm(forms.Form):
    set_name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter a name for this document set'})
    )
    documents = MultipleFileField(required=True)

class DocumentSetSelectForm(forms.Form):
    document_set = forms.ModelChoiceField(queryset=None, empty_label=None)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['document_set'].queryset = DocumentSet.objects.filter(user=user)