from django import forms
from django.core.validators import MinLengthValidator, RegexValidator
from .models import Issue


class IssueForm(forms.ModelForm):
    summary = forms.CharField(
        label='Краткое описание',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[
            MinLengthValidator(5, message='Заголовок должен быть минимум 5 символов'),
            RegexValidator(r'^[A-Z]', message='Заголовок должен начинаться с заглавной буквы'),
        ]
    )

    class Meta:
        model = Issue
        fields = ['summary', 'description', 'status', 'types']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'types': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'description': 'Полное описание',
            'status': 'Статус',
            'types': 'Типы',
        }