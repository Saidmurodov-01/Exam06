from rest_framework import viewsets
from rest_framework.response import Response
from .models import Score
from .serializers import ScoreSerializer

class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.select_related('game', 'player').all()   # 🔑 qo‘shildi
    serializer_class = ScoreSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        game_id = self.request.query_params.get('game_id')
        player_id = self.request.query_params.get('player_id')
        result = self.request.query_params.get('result')

        if game_id:
            qs = qs.filter(game_id=game_id)
        if player_id:
            qs = qs.filter(player_id=player_id)
        if result in ('win', 'draw', 'loss'):
            qs = qs.filter(result=result)
        return qs

    def destroy(self, request, *args, **kwargs):
        score = self.get_object()
        player = score.player
        resp = super().destroy(request, *args, **kwargs)
        # ratingni qayta hisoblash
        player.rating = max(0, player.rating - score.points)
        player.save(update_fields=['rating'])
        return resp