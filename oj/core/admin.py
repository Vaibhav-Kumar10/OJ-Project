from django.contrib import admin
from .models import Problem, TestCase, Submission


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ["title", "difficulty", "score", "is_complete"]
    search_fields = ["title", "tags"]
    list_filter = ["difficulty", "is_complete"]


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ["problem", "id"]
    search_fields = ["problem__title"]


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ["user", "problem", "verdict", "language", "submitted_at"]
    list_filter = ["verdict", "language"]
    search_fields = ["user__username", "problem__title"]
