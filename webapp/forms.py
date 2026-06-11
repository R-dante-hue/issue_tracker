from django import forms
from .models import Issue


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['summary', 'description', 'status', 'types']
        widgets = {
            'summary': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'types': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'summary': 'Краткое описание',
            'description': 'Полное описание',
            'status': 'Статус',
            'types': 'Типы',
        }