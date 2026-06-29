from django.urls import path
from webapp.views.projects import (
    ProjectListView, ProjectDetailView, ProjectCreateView,
    ProjectUpdateView, ProjectDeleteView, ProjectIssueCreateView,
    ProjectUserAddView, ProjectUserRemoveView,
)
from webapp.views.issues import (
    IssueDetailView, IssueUpdateView, IssueDeleteView,
)

urlpatterns = [
    path('', ProjectListView.as_view(), name='project_list'),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('project/create/', ProjectCreateView.as_view(), name='project_create'),
    path('project/<int:pk>/edit/', ProjectUpdateView.as_view(), name='project_update'),
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
    path('project/<int:pk>/issue/create/', ProjectIssueCreateView.as_view(), name='project_issue_create'),
    path('issue/<int:pk>/', IssueDetailView.as_view(), name='issue_detail'),
    path('issue/<int:pk>/edit/', IssueUpdateView.as_view(), name='issue_update'),
    path('issue/<int:pk>/delete/', IssueDeleteView.as_view(), name='issue_delete'),
    path('project/<int:pk>/users/add/', ProjectUserAddView.as_view(), name='project_user_add'),
path('project/<int:pk>/users/<int:user_pk>/remove/', ProjectUserRemoveView.as_view(), name='project_user_remove'),
]