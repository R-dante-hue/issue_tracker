from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from webapp.models import Project, Issue
from webapp.forms import ProjectForm, IssueForm


class ProjectListView(ListView):
    template_name = 'webapp/projects/list.html'
    model = Project
    context_object_name = 'projects'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return Project.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        return Project.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


class ProjectDetailView(DetailView):
    template_name = 'webapp/projects/detail.html'
    model = Project
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['issues'] = self.object.issues.filter(is_deleted=False)
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    template_name = 'webapp/projects/form.html'
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy('project_list')


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'webapp/projects/form.html'
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy('project_list')


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'webapp/projects/delete.html'
    model = Project
    success_url = reverse_lazy('project_list')


class ProjectIssueCreateView(LoginRequiredMixin, CreateView):
    template_name = 'webapp/issues/form.html'
    model = Issue
    form_class = IssueForm

    def form_valid(self, form):
        project = Project.objects.get(pk=self.kwargs['pk'])
        form.instance.project = project
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.object.project.pk})