from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Count, Q
from .models import Player
from .serializers import PlayerSerializer

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    def get_queryset(self):
        qs = Player.objects.all().annotate(
            total_games=Count('scores'),
            wins=Count('scores', filter=Q(scores__result='win')),
            draws=Count('scores', filter=Q(scores__result='draw')),
            losses=Count('scores', filter=Q(scores__result='loss')),
        )
        country = self.request.query_params.get('country')
        min_rating = self.request.query_params.get('min_rating')
        search = self.request.query_params.get('search')

        if country:
            qs = qs.filter(country__iexact=country)
        if min_rating:
            try:
                qs = qs.filter(rating__gte=int(min_rating))
            except ValueError:
                pass
        if search:
            qs = qs.filter(nickname__icontains=search)
        return qs

    def destroy(self, request, *args, **kwargs):
        player = self.get_object()
        if player.scores.exists():
            return Response(
                {'error': f'Cannot delete player with game history. Player has {player.scores.count()} recorded games.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)