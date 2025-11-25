from rest_framework import serializers

class LeaderboardEntrySerializer(serializers.Serializer):
    player = serializers.CharField()
    country = serializers.CharField()
    rating = serializers.IntegerField()
    points = serializers.IntegerField()
    wins = serializers.IntegerField()
    draws = serializers.IntegerField()
    losses = serializers.IntegerField()
    rank = serializers.IntegerField()
