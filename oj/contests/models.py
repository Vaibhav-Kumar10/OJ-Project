from django.db import models
from core.models import Problem
from django.conf import settings


class UserScore(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    problems_solved = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.score} pts"


class ProblemCompletion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    is_complete = models.BooleanField(default=False)
    score_awarded = models.IntegerField(default=0)

    # To make a composite primary key
    class Meta:
        unique_together = ("user", "problem")
