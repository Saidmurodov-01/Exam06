from django.urls import path, include
from rest_framework.routers import DefaultRouter
from games.views import GameViewSet
from players.views import PlayerViewSet
from scores.views import ScoreViewSet

router = DefaultRouter()
router.register(r'games', GameViewSet)
router.register(r'players', PlayerViewSet)
router.register(r'scores', ScoreViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('leaderboard/', include('leaderboard.urls')),
]