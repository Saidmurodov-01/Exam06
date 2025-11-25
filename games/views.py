from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Game
from .serializers import GameSerializer

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def destroy(self, request, *args, **kwargs):
        game = self.get_object()
        if game.scores.exists():
            return Response(
                {'error': 'Cannot delete game with existing scores. Tournament has active games.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)