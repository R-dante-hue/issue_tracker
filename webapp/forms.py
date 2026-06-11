from django import forms
from .models import Issue, Status, Type


class IssueForm(forms.ModelForm):
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Статус'
    )
    issue_type = forms.ModelChoiceField(
        queryset=Type.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Тип'
    )

    class Meta:
        model = Issue
        fields = ['summary', 'description', 'status', 'issue_type']
        widgets = {
            'summary': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
        labels = {
            'summary': 'Краткое описание',
            'description': 'Полное описание',
        }