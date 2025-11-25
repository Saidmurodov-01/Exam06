from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Count, Q
from games.models import Game
from players.models import Player
from scores.models import Score

class GameLeaderboardView(APIView):
    def get(self, request):
        game_id = request.query_params.get('game_id')
        if not game_id:
            return Response({'error': 'game_id is required'}, status=400)

        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return Response({'error': 'Game not found'}, status=404)

        agg = Score.objects.filter(game_id=game_id).values('player_id').annotate(
            points=Sum('points'),
            wins=Count('id', filter=Q(result='win')),
            draws=Count('id', filter=Q(result='draw')),
            losses=Count('id', filter=Q(result='loss')),
        ).order_by('-points')

        leaderboard = []
        rank = 1
        players = {p.id: p for p in Player.objects.filter(id__in=[a['player_id'] for a in agg])}
        for row in agg:
            p = players[row['player_id']]
            leaderboard.append({
                'rank': rank,
                'player': p.nickname,
                'player_id': p.id,
                'country': p.country,
                'rating': p.rating,
                'points': row['points'] or 0,
                'wins': row['wins'],
                'draws': row['draws'],
                'losses': row['losses'],
                'rating_change': row['points'] or 0,
            })
            rank += 1

        return Response(leaderboard, status=200)

class TopPlayersLeaderboardView(APIView):
    def get(self, request):
        game_id = request.query_params.get('game_id')
        limit = int(request.query_params.get('limit', 10))
        if not game_id:
            return Response({'error': 'game_id is required'}, status=400)

        try:
            game = Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return Response({'error': 'Game not found'}, status=404)

        agg = Score.objects.filter(game_id=game_id).values('player_id').annotate(
            points=Sum('points'),
        ).order_by('-points')[:limit]

        players = {p.id: p for p in Player.objects.filter(id__in=[a['player_id'] for a in agg])}

        leaderboard = []
        for i, row in enumerate(agg, start=1):
            p = players[row['player_id']]
            leaderboard.append({
                'rank': i,
                'player': p.nickname,
                'country': p.country,
                'rating': p.rating,
                'points': row['points'] or 0,
            })

        return Response({
            'game_id': game.id,
            'game_title': game.title,
            'limit': limit,
            'total_players': Score.objects.filter(game_id=game_id).values('player_id').distinct().count(),
            'leaderboard': leaderboard
        }, status=200)

class GlobalLeaderboardView(APIView):
    def get(self, request):
        country = request.query_params.get('country')
        limit = int(request.query_params.get('limit', 100))

        qs = Player.objects.all()
        if country:
            qs = qs.filter(country__iexact=country)
        qs = qs.order_by('-rating')[:limit]

        data = []
        for i, p in enumerate(qs, start=1):
            data.append({
                'rank': i,
                'player': p.nickname,
                'rating': p.rating,
                'total_games': p.scores.count(),
            })

        return Response({
            'total_players': Player.objects.count() if not country else Player.objects.filter(country__iexact=country).count(),
            'country': country,
            'leaderboard': data
        }, status=200)