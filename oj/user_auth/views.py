from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()


def signup_view(request):
    """
    Render the signup page of the OJ application.
    """
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        username = request.POST.get("uname")
        mobile_no = request.POST.get("mobile_no")
        dob = request.POST.get("dob")
        password = request.POST.get("password")
        repassword = request.POST.get("repassword")

        # Validate the input fields
        if (
            not fname
            or not lname
            or not email
            or not username
            or not password
            or not repassword
        ):
            messages.error(request, "All fields are required.")
            return render(request, "user_auth/signup.html")

        if password != repassword:
            messages.error(request, "Passwords do not match.")
            return render(request, "user_auth/signup.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "user_auth/signup.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, "user_auth/signup.html")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=fname,
            last_name=lname,
            mobile_no=mobile_no,
            dob=dob,
        )
        login(request, user)
        return redirect("core:dashboard")

    return render(request, "user_auth/signup.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("uname")
        password = request.POST.get("password")

        # Validate the input fields
        if not username or not password:
            messages.error(request, "Username and password are required.")
            return redirect("user_auth:login")

        user = authenticate(request, username=username, password=password)

        # Check if the user is authenticated
        if user is not None:
            login(request, user)
            return redirect("core:dashboard")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("user_auth:login")
    return render(request, "user_auth/login.html")


def logout_view(request):
    """
    Handle user logout in the OJ application.
    """
    logout(request)
    return redirect("user_auth:login")
