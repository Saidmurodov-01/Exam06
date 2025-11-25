from django.contrib import admin
from .models import Score

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('game', 'player', 'result', 'points', 'created_at')
    list_filter = ('result', 'game')
    search_fields = ('player__nickname', 'opponent_name')
