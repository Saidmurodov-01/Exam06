from rest_framework import serializers
from .models import Score, POINTS_MAP
from games.models import Game
from players.models import Player

class NestedGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'title', 'location']

class NestedPlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'nickname', 'country']

class ScoreSerializer(serializers.ModelSerializer):
    game_detail = NestedGameSerializer(source='game', read_only=True)
    player_detail = NestedPlayerSerializer(source='player', read_only=True)

    class Meta:
        model = Score
        fields = ['id', 'game', 'player', 'result', 'points', 'opponent_name', 'created_at', 'game_detail', 'player_detail']
        read_only_fields = ['points', 'created_at', 'game_detail', 'player_detail']

    def create(self, validated_data):
        score = super().create(validated_data)
        player = score.player
        player.rating += score.points
        player.save(update_fields=['rating'])
        return score

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['game'] = data.pop('game_detail')
        data['player'] = data.pop('player_detail')
        return data