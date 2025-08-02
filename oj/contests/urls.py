from django.urls import path
from .views import leaderboard_view, contests_view

app_name = "contests"


urlpatterns = [
    path("contest/", contests_view, name="contest"),
    path("leaderboard/", leaderboard_view, name="leaderboard"),
]
