from django.urls import path
from .views import GameLeaderboardView, TopPlayersLeaderboardView, GlobalLeaderboardView

urlpatterns = [
    path('', GameLeaderboardView.as_view(), name='leaderboard-game'),
    path('top/', TopPlayersLeaderboardView.as_view(), name='leaderboard-top'),
    path('global/', GlobalLeaderboardView.as_view(), name='leaderboard-global'),
]