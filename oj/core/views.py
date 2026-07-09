from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Problem, Submission
from contests.models import ProblemCompletion, UserScore
from google import genai
import markdown
import os
from django.contrib.auth.models import User
from django.db.models import Count
from datetime import datetime, timedelta
import json
from django.contrib.auth import get_user_model


# ----------------- Home Page ----------------- #
def home_view(request):
    featured_problems = []
    recent_submissions = []

    if request.user.is_authenticated:
        featured_problems = (
            ProblemCompletion.objects.filter(user=request.user, is_complete=True)
            .select_related("problem")
            .order_by("-score_awarded")[:4]
        )

        # Get recent submissions for the authenticated user
        recent_submissions = (
            Submission.objects.filter(user=request.user)
            .select_related("problem")
            .order_by("-submitted_at")[:5]  # Get last 5 submissions
        )

    scores = UserScore.objects.select_related("user").order_by(
        "-score", "-problems_solved"
    )

    context = {
        "featured_problems": featured_problems,
        "recent_submissions": recent_submissions,
        "scores": scores,
    }

    return render(request, "core/home.html", context)


# ----------------- List All Problems ----------------- #
def all_problems_view(request):
    problems = Problem.objects.all()
    
    difficulty = request.GET.get('difficulty')
    category = request.GET.get('category')
    status = request.GET.get('status')
    search = request.GET.get('search')
    sort_by = request.GET.get('sort')

    if difficulty:
        problems = problems.filter(difficulty__iexact=difficulty)
    
    if category:
        problems = problems.filter(tags__icontains=category)
        
    if search:
        problems = problems.filter(title__icontains=search)
        
    if status and request.user.is_authenticated:
        user_submissions = Submission.objects.filter(user=request.user)
        if status == 'solved':
            solved_ids = user_submissions.filter(verdict='Accepted').values_list('problem_id', flat=True)
            problems = problems.filter(id__in=solved_ids)
        elif status == 'attempted':
            solved_ids = user_submissions.filter(verdict='Accepted').values_list('problem_id', flat=True)
            attempted_ids = user_submissions.exclude(verdict='Accepted').values_list('problem_id', flat=True)
            problems = problems.filter(id__in=attempted_ids).exclude(id__in=solved_ids)
        elif status == 'unsolved':
            attempted_ids = user_submissions.values_list('problem_id', flat=True)
            problems = problems.exclude(id__in=attempted_ids)

    if sort_by:
        if sort_by == 'difficulty':
            from django.db.models import Case, When, Value, IntegerField
            problems = problems.annotate(
                diff_order=Case(
                    When(difficulty__iexact='easy', then=Value(1)),
                    When(difficulty__iexact='medium', then=Value(2)),
                    When(difficulty__iexact='hard', then=Value(3)),
                    default=Value(4),
                    output_field=IntegerField(),
                )
            ).order_by('diff_order', 'title')
        elif sort_by == 'title':
            problems = problems.order_by('title')
        elif sort_by == 'score':
            problems = problems.order_by('-score', 'title')

    return render(request, "core/allproblems.html", {"problems": problems})


# ----------------- Problem Detail View ----------------- #
@login_required
def problem_view(request, id):
    problem = get_object_or_404(Problem, id=id)
    user_submissions = Submission.objects.filter(
        user=request.user, problem=problem
    ).order_by("-submitted_at")

    problem.tag_list = problem.tags.split() if problem.tags else []

    context = {"problem": problem, "submissions": user_submissions}
    return render(request, "core/problem_detail.html", context=context)


@login_required
def get_ai_review(request):
    if request.method == "POST":
        code = request.POST.get("code")
        language = request.POST.get("language")
        problem_id = request.POST.get("problem_id")
        input_data = request.POST.get("input_data", "")
        problem = get_object_or_404(Problem, id=problem_id)

        try:
            # The client gets the API key from the environment variable `GEMINI_API_KEY`.
            client = genai.Client()

            prompt = (
                "You're an expert code reviewer.\n"
                "Given the following code and problem statement, provide a short, clear review focusing on performance, style, and correctness.\n"
                f"Problem:\n{problem.statement}\n"
                f"Code ({language}):\n{code}"
            )
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )

            ai_review = response.text

        except Exception as e:
            ai_review = f"⚠️ AI Review failed: {str(e)}"

        ai_review = markdown.markdown(ai_review)

        # Pull previous submissions
        submissions = Submission.objects.filter(
            user=request.user, problem=problem
        ).order_by("-submitted_at")

        return render(
            request,
            "core/problem_detail.html",
            {
                "problem": problem,
                "submissions": submissions,
                "code": code,
                "language": language,
                "input_data": input_data,
                "ai_review": ai_review,
            },
        )

    return redirect("core:problems")


def generate_submission_calendar(user):
    """Generate calendar data for submissions"""
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=365)

    # Get all submissions in the last year
    submissions = (
        Submission.objects.filter(
            user=user,
            submitted_at__date__gte=start_date,
            submitted_at__date__lte=end_date,
        )
        .values("submitted_at__date")
        .annotate(count=Count("id"))
    )

    # Convert to dictionary for easy lookup
    calendar_data = {}
    for submission in submissions:
        date_str = submission["submitted_at__date"].strftime("%Y-%m-%d")
        calendar_data[date_str] = submission["count"]

    return calendar_data


# Get your custom User model
User = get_user_model()


@login_required
def profile_view(request, username=None):
    # If no username provided, show current user's profile
    if username:
        profile_user = get_object_or_404(User, username=username)
    else:
        profile_user = request.user

    # Get user score
    try:
        user_score = UserScore.objects.get(user=profile_user)
    except UserScore.DoesNotExist:
        user_score = UserScore(user=profile_user, score=0, problems_solved=0)

    # Get difficulty statistics
    completed_problems = ProblemCompletion.objects.filter(
        user=profile_user, is_complete=True
    ).select_related("problem")

    difficulty_stats = {
        "easy": completed_problems.filter(problem__difficulty__iexact="easy").count(),
        "medium": completed_problems.filter(
            problem__difficulty__iexact="medium"
        ).count(),
        "hard": completed_problems.filter(problem__difficulty__iexact="hard").count(),
    }

    # Get recent submissions (last 10)
    recent_submissions = (
        Submission.objects.filter(user=profile_user)
        .select_related("problem")
        .order_by("-submitted_at")[:10]
    )

    # Calculate current streak
    current_streak = calculate_streak(profile_user)

    # Get language statistics
    language_stats = dict(
        Submission.objects.filter(user=profile_user)
        .values("language")
        .annotate(count=Count("language"))
        .values_list("language", "count")
    )

    # Generate submission calendar data
    submission_calendar = generate_submission_calendar(profile_user)

    submission_calendar = {
        str(date): count for date, count in submission_calendar.items()
    }

    # Calculate age from date of birth
    age = None
    if profile_user.dob:
        today = datetime.now().date()
        age = today.year - profile_user.dob.year
        if today < profile_user.dob.replace(year=today.year):
            age -= 1

    context = {
        "profile_user": profile_user,
        "user_score": user_score,
        "difficulty_stats": difficulty_stats,
        "recent_submissions": recent_submissions,
        "current_streak": current_streak,
        "language_stats": language_stats,
        "submission_calendar": json.dumps(submission_calendar),
        "user_age": age,
    }

    badges = [
        {
            "icon": "🎯",
            "title": "First Solve",
            "description": "Solve your first problem",
            "condition": user_score.problems_solved > 0,
        },
        {
            "icon": "💡",
            "title": "Problem Solver",
            "description": "Solve 10+ problems",
            "condition": user_score.problems_solved >= 10,
        },
    ]
    context["badges"] = badges

    return render(request, "core/profile.html", context)


def calculate_streak(user):
    """Calculate current solving streak for a user"""
    today = datetime.now().date()
    streak = 0
    current_date = today

    while True:
        # Check if user has any accepted submissions on current_date
        has_submission = Submission.objects.filter(
            user=user, verdict="Accepted", submitted_at__date=current_date
        ).exists()

        if has_submission:
            streak += 1
            current_date -= timedelta(days=1)
        else:
            break

    return streak
