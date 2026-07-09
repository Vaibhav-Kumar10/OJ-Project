from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from django.contrib import messages
import uuid

User = get_user_model()

# In-memory token store for password reset (keyed by token -> user pk)
# For production use Django's built-in PasswordResetView with an email backend.
_reset_tokens = {}


def signup_view(request):
    """
    Render the signup page of the OJ application.
    """
    if request.user.is_authenticated:
        return redirect("core:profile")
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
        return redirect("core:profile")

    return render(request, "user_auth/signup.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("core:profile")
    if request.method == "POST":
        identifier = request.POST.get("uname")  # username or email
        password = request.POST.get("password")

        # Validate the input fields
        if not identifier or not password:
            messages.error(request, "Username/email and password are required.")
            return redirect("user_auth:login")

        # If the identifier looks like an email, resolve to username
        if "@" in identifier:
            try:
                user_obj = User.objects.get(email__iexact=identifier)
                identifier = user_obj.username
            except User.DoesNotExist:
                messages.error(request, "Invalid username or password.")
                return redirect("user_auth:login")

        user = authenticate(request, username=identifier, password=password)

        remember = request.POST.get("remember_me")
        if remember:
            request.session.set_expiry(1209600)  # 2 weeks
        else:
            request.session.set_expiry(0)  # Expires on browser close

        # Check if the user is authenticated
        if user is not None:
            login(request, user)
            return redirect("core:profile")
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


def forgot_password_view(request):
    """
    Allow user to request a password reset by entering their email.
    Generates a one-time token stored in memory and redirects to reset page.
    """
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        if not email:
            messages.error(request, "Please enter your email address.")
            return render(request, "user_auth/forgot_password.html")

        try:
            user = User.objects.get(email__iexact=email)
            token = str(uuid.uuid4())
            _reset_tokens[token] = user.pk
            messages.success(
                request,
                "A password reset link has been generated. "
                "Click the link below to reset your password.",
            )
            return redirect("user_auth:reset_password", token=token)
        except User.DoesNotExist:
            # Don't reveal whether email exists
            messages.info(
                request,
                "If that email is registered, a reset link will appear.",
            )
            return render(request, "user_auth/forgot_password.html")

    return render(request, "user_auth/forgot_password.html")


def reset_password_view(request, token):
    """
    Handle the actual password reset using a one-time token.
    """
    user_pk = _reset_tokens.get(token)
    if user_pk is None:
        messages.error(request, "This password reset link is invalid or has expired.")
        return redirect("user_auth:forgot_password")

    if request.method == "POST":
        password = request.POST.get("password", "")
        repassword = request.POST.get("repassword", "")

        if not password or not repassword:
            messages.error(request, "Both password fields are required.")
            return render(request, "user_auth/reset_password.html", {"token": token})

        if password != repassword:
            messages.error(request, "Passwords do not match.")
            return render(request, "user_auth/reset_password.html", {"token": token})

        try:
            user = User.objects.get(pk=user_pk)
            user.set_password(password)
            user.save()
            # Invalidate the token after use
            del _reset_tokens[token]
            messages.success(request, "Password reset successful! Please sign in.")
            return redirect("user_auth:login")
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect("user_auth:forgot_password")

    return render(request, "user_auth/reset_password.html", {"token": token})
