from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from webapp.models import Issue
from webapp.forms import IssueForm


class IssueDetailView(DetailView):
    template_name = 'webapp/issues/detail.html'
    model = Issue
    context_object_name = 'issue'

    def get_queryset(self):
        return Issue.objects.filter(is_deleted=False)


class IssueUpdateView(UserPassesTestMixin, UpdateView):
    template_name = 'webapp/issues/form.html'
    model = Issue
    form_class = IssueForm

    def test_func(self):
        issue = self.get_object()
        user = self.request.user
        return issue.project.users.filter(pk=user.pk).exists()

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.object.project.pk})


class IssueDeleteView(UserPassesTestMixin, DeleteView):
    template_name = 'webapp/issues/delete.html'
    model = Issue

    def test_func(self):
        issue = self.get_object()
        user = self.request.user
        return issue.project.users.filter(pk=user.pk).exists()

    def post(self, request, *args, **kwargs):
        issue = self.get_object()
        issue.is_deleted = True
        issue.save()
        return redirect('project_detail', pk=issue.project.pk)

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.object.project.pk})