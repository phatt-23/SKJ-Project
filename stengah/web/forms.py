from django import forms

from common.models import Commit


class CommitUploadForm(forms.ModelForm):
    message = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Commit message',
            'class': 'form-control mb-2',
        })
    )

    files = forms.FileField(
        widget=forms.TextInput(attrs={
            'name': 'files',
            'type': 'file',
            'class': 'form-control mb-2',
            'multiple': 'True',
        }),
        required=False,
        label='Upload text files'
    )

    class Meta:
        model = Commit 
        fields = ['message', 'files']



