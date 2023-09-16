from django.urls import path, include
from teams.views import TeamsView, TeamDetailView

urlpatterns = [
    path("teams/", TeamsView.as_view()),
    path("teams/<int:team_id>/", TeamDetailView.as_view()),
]
