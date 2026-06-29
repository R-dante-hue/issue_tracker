from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
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
        context['all_users'] = User.objects.all()
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    template_name = 'webapp/projects/form.html'
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy('project_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.users.add(self.request.user)
        return response


class ProjectUpdateView(UserPassesTestMixin, UpdateView):
    template_name = 'webapp/projects/form.html'
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy('project_list')

    def test_func(self):
        project = self.get_object()
        user = self.request.user
        return project.users.filter(pk=user.pk).exists() or user.groups.filter(name='Project Manager').exists()


class ProjectDeleteView(UserPassesTestMixin, DeleteView):
    template_name = 'webapp/projects/delete.html'
    model = Project
    success_url = reverse_lazy('project_list')

    def test_func(self):
        project = self.get_object()
        user = self.request.user
        return project.users.filter(pk=user.pk).exists() or user.groups.filter(name='Project Manager').exists()


class ProjectIssueCreateView(UserPassesTestMixin, CreateView):
    template_name = 'webapp/issues/form.html'
    model = Issue
    form_class = IssueForm

    def test_func(self):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        user = self.request.user
        return project.users.filter(pk=user.pk).exists()

    def form_valid(self, form):
        project = Project.objects.get(pk=self.kwargs['pk'])
        form.instance.project = project
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.object.project.pk})


class ProjectUserAddView(UserPassesTestMixin, View):
    def test_func(self):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        user = self.request.user
        return project.users.filter(pk=user.pk).exists() or user.groups.filter(name='Project Manager').exists()

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        user_id = request.POST.get('user_id')
        if user_id:
            user = get_object_or_404(User, pk=user_id)
            project.users.add(user)
        return redirect('project_detail', pk=pk)


class ProjectUserRemoveView(UserPassesTestMixin, View):
    def test_func(self):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        user = self.request.user
        return project.users.filter(pk=user.pk).exists() or user.groups.filter(name='Project Manager').exists()

    def post(self, request, pk, user_pk):
        project = get_object_or_404(Project, pk=pk)
        user = get_object_or_404(User, pk=user_pk)
        project.users.remove(user)
        return redirect('project_detail', pk=pk)