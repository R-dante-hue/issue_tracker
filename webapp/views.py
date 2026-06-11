from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, ListView, DetailView, CreateView, UpdateView, DeleteView
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


class IssueUpdateView(UpdateView):
    template_name = 'webapp/issue_form.html'
    model = Issue
    form_class = IssueForm
    success_url = reverse_lazy('index')


class IssueDeleteView(DeleteView):
    template_name = 'webapp/issue_delete.html'
    model = Issue
    success_url = reverse_lazy('index')