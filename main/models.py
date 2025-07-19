# models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Game(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', '대기중'
        COMPLETED = 'COMPLETED', '종료됨'

    attacker = models.ForeignKey(User, related_name='games_attacked', on_delete=models.CASCADE)
    defender = models.ForeignKey(User, related_name='games_defended', on_delete=models.CASCADE)
    attacker_card = models.PositiveSmallIntegerField(null=True, blank=True)
    defender_card = models.PositiveSmallIntegerField(null=True, blank=True)

    winner = models.ForeignKey(User, related_name='games_won', null=True, blank=True, on_delete=models.SET_NULL)
    loser = models.ForeignKey(User, related_name='games_lost', null=True, blank=True, on_delete=models.SET_NULL)

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    attacker_score_change = models.IntegerField(default=0)  # type: ignore
    defender_score_change = models.IntegerField(default=0)  # type: ignore

    is_deleted_by_attacker = models.BooleanField(default=False)  # type: ignore

    def is_draw(self):
        return (
            self.attacker_card is not None and
            self.defender_card is not None and
            self.attacker_card == self.defender_card
        )

    def can_cancel(self, user):
        return self.attacker == user and self.status == self.Status.PENDING

    def can_counter(self, user):
        return self.defender == user and self.status == self.Status.PENDING and self.defender_card is None

    def get_result_summary(self):
        if self.status == self.Status.PENDING:
            return "진행중.."
        elif self.is_draw():
            return "무승부"
        else:
            return f"{self.winner.username} 승리"  # type: ignore
