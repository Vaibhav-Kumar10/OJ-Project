from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()




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
    Multi-step password reset:
      Step 1 – Enter email (GET / first POST)
      Step 2 – Enter date of birth to verify identity
      Step 3 – Enter new password
    State is kept in the session (no email sending required).
    """
    step = request.session.get("fp_step", 1)

    if request.method == "POST":
        action = request.POST.get("action", "")

        # ── Step 1: verify email ──────────────────────────────────────────
        if action == "verify_email":
            email = request.POST.get("email", "").strip()
            if not email:
                messages.error(request, "Please enter your email address.")
                request.session["fp_step"] = 1
                return render(request, "user_auth/forgot_password.html", {"step": 1})

            try:
                user = User.objects.get(email__iexact=email)
                # Store only the PK — never the password
                request.session["fp_user_pk"] = user.pk
                request.session["fp_step"] = 2
                return render(request, "user_auth/forgot_password.html", {"step": 2})
            except User.DoesNotExist:
                messages.error(request, "No account found with that email address.")
                request.session["fp_step"] = 1
                return render(request, "user_auth/forgot_password.html", {"step": 1})

        # ── Step 2: verify date of birth ─────────────────────────────────
        elif action == "verify_dob":
            user_pk = request.session.get("fp_user_pk")
            if not user_pk:
                messages.error(request, "Session expired. Please start again.")
                request.session["fp_step"] = 1
                return render(request, "user_auth/forgot_password.html", {"step": 1})

            dob_input = request.POST.get("dob", "").strip()
            if not dob_input:
                messages.error(request, "Please enter your date of birth.")
                return render(request, "user_auth/forgot_password.html", {"step": 2})

            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                messages.error(request, "Session expired. Please start again.")
                request.session["fp_step"] = 1
                return render(request, "user_auth/forgot_password.html", {"step": 1})

            if user.dob is None:
                messages.error(request, "This account has no date of birth set. Please contact support.")
                return render(request, "user_auth/forgot_password.html", {"step": 2})

            from datetime import date
            try:
                entered_dob = date.fromisoformat(dob_input)
            except ValueError:
                messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
                return render(request, "user_auth/forgot_password.html", {"step": 2})

            if entered_dob != user.dob:
                messages.error(request, "Date of birth does not match our records.")
                return render(request, "user_auth/forgot_password.html", {"step": 2})

            # DOB verified — proceed to step 3
            request.session["fp_step"] = 3
            return render(request, "user_auth/forgot_password.html", {"step": 3})

        # ── Step 3: set new password ──────────────────────────────────────
        elif action == "set_password":
            user_pk = request.session.get("fp_user_pk")
            if not user_pk or request.session.get("fp_step") != 3:
                messages.error(request, "Session expired. Please start again.")
                request.session["fp_step"] = 1
                return render(request, "user_auth/forgot_password.html", {"step": 1})

            password = request.POST.get("password", "")
            repassword = request.POST.get("repassword", "")

            if not password or not repassword:
                messages.error(request, "Both password fields are required.")
                return render(request, "user_auth/forgot_password.html", {"step": 3})

            if password != repassword:
                messages.error(request, "Passwords do not match.")
                return render(request, "user_auth/forgot_password.html", {"step": 3})

            try:
                user = User.objects.get(pk=user_pk)
                user.set_password(password)
                user.save()
                # Clear session state
                for key in ("fp_user_pk", "fp_step"):
                    request.session.pop(key, None)
                messages.success(request, "Password reset successful! Please sign in.")
                return redirect("user_auth:login")
            except User.DoesNotExist:
                messages.error(request, "User not found. Please start again.")
                request.session["fp_step"] = 1
                return render(request, "user_auth/forgot_password.html", {"step": 1})

    # GET request — always start at step 1
    for key in ("fp_user_pk", "fp_step"):
        request.session.pop(key, None)
    return render(request, "user_auth/forgot_password.html", {"step": 1})


def reset_password_view(request, token):
    """
    Legacy token-based reset – kept for URL compatibility but redirects
    to the new multi-step forgot-password flow.
    """
    messages.info(request, "Please use the form below to reset your password.")
    return redirect("user_auth:forgot_password")

