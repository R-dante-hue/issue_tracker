from django.contrib.auth import login
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .forms import MyUserCreationForm


class RegisterView(CreateView):
    model = User
    template_name = 'accounts/register.html'
    form_class = MyUserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse_lazy('project_list')
        return next_url