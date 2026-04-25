"""URL mappings for the student app."""
from django.urls import path
from student import views

app_name = 'student'

urlpatterns = [
    path(
        'skills/',
        views.SkillListView.as_view(),
        name='skill-list',
    ),
    path(
        'me/skills/',
        views.MySkillListView.as_view(),
        name='my-skills',
    ),
    path(
        'me/skills/add/',
        views.AddSkillView.as_view(),
        name='add-skill',
    ),
    path(
        'me/skills/<int:pk>/remove/',
        views.RemoveSkillView.as_view(),
        name='remove-skill',
    ),
]