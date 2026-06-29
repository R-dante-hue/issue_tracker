from django import forms
from django.contrib.auth.models import User


class MyUserCreationForm(forms.ModelForm):
    password = forms.CharField(
        label="Пароль",
        strip=False,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password_confirm = forms.CharField(
        label="Подтвердите пароль",
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password_confirm']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': 'required'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name', '').strip()
        last_name = cleaned_data.get('last_name', '').strip()
        if not first_name and not last_name:
            raise forms.ValidationError('Заполните хотя бы одно из полей: Имя или Фамилия')
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают!')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user