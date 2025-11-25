from rest_framework import serializers
from .models import Game

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'title', 'location', 'start_date', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']