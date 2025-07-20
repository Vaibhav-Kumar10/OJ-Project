from django.db import models
from django.conf import settings


class Problem(models.Model):
    title = models.CharField(max_length=200)
    statement = models.TextField()
    difficulty = models.CharField(max_length=50)
    input_example = models.TextField()
    output_example = models.TextField()
    tags = models.TextField()
    score = models.IntegerField()
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class TestCase(models.Model):
    problem = models.ForeignKey(
        Problem, on_delete=models.CASCADE, related_name="testcases"
    )
    input = models.TextField()
    output = models.TextField()

    def __str__(self):
        return f"TestCase for {self.problem.title}"


class Submission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    code = models.TextField()
    verdict = models.CharField(max_length=50)
    language = models.CharField(max_length=50)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.problem.title} - {self.verdict}"
