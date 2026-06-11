from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Issue
from .forms import IssueForm


class IndexView(ListView):
    template_name = 'webapp/index.html'
    model = Issue
    context_object_name = 'issues'
    ordering = ['-created_at']


class IssueDetailView(DetailView):
    template_name = 'webapp/issue_detail.html'
    model = Issue
    context_object_name = 'issue'


class IssueCreateView(CreateView):
    template_name = 'webapp/issue_form.html'
    model = Issue
    form_class = IssueForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        types = form.cleaned_data.pop('types')
        self.object = form.save()
        self.object.types.set(types)
        return redirect(self.get_success_url())


class IssueUpdateView(UpdateView):
    template_name = 'webapp/issue_form.html'
    model = Issue
    form_class = IssueForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        types = form.cleaned_data.pop('types')
        self.object = form.save()
        self.object.types.set(types)
        return redirect(self.get_success_url())


class IssueDeleteView(DeleteView):
    template_name = 'webapp/issue_delete.html'
    model = Issue
    success_url = reverse_lazy('index')