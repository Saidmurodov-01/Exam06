from django.db import models
from django.core.exceptions import ValidationError
from games.models import Game
from players.models import Player

RESULT_CHOICES = (
    ('win', 'win'),
    ('draw', 'draw'),
    ('loss', 'loss'),
)

POINTS_MAP = {
    'win': 10,
    'draw': 5,
    'loss': 0,
}

class Score(models.Model):
    game = models.ForeignKey(Game, on_delete=models.PROTECT, related_name='scores')
    player = models.ForeignKey(Player, on_delete=models.PROTECT, related_name='scores')
    result = models.CharField(max_length=10, choices=RESULT_CHOICES)
    points = models.IntegerField()
    opponent_name = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        if self.result not in dict(RESULT_CHOICES):
            raise ValidationError({'result': 'Result must be one of: win, draw, loss.'})

    def save(self, *args, **kwargs):
       
        self.points = POINTS_MAP.get(self.result, 0)
        super().save(*args, **kwargs)