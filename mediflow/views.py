# mediflow/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from functools import wraps
from .forms import MedicineForm
from .models import User, NGOProfile , Medicine, Pickup, NGORequest
User = get_user_model()

# -------------------------
# Helper decorator: restrict access by role
# -------------------------
def role_required(allowed_roles=None, redirect_to='login'):
    if allowed_roles is None:
        allowed_roles = []
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, "Please login first.")
                return redirect(redirect_to)
            if request.user.user_type not in allowed_roles:
                messages.error(request, "You are not authorized to view that page.")
                # redirect to an appropriate place based on role
                if request.user.user_type == "ngo":
                    return redirect('NGOdashboard')
                return redirect('dashboard')
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator

# -------------------------
# Public pages
# -------------------------
def landing(request):
    return render(request, 'landing.html')

# -------------------------
# Donor registration
# -------------------------
def register(request):
    if request.method == "POST":
        fullname = request.POST.get("fullname", "").strip()
        phone = request.POST.get("phone", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")

        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return render(request, "registration.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, "registration.html")

        user = User.objects.create_user(
            fullname=fullname,
            phone=phone,
            email=email,
            user_type="donor",
            password=password
        )

        messages.success(request, "Account created successfully! Please login.")
        return redirect("login")

    return render(request, "registration.html")


# -------------------------
# Donor login
# -------------------------
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)
        if user is None:
            messages.error(request, "Invalid email or password.")
            return render(request, "login.html")

        # role check: donor-only login page
        if user.user_type != "donor":
            messages.error(request, "This login page is for Donors only. Use NGO login if you're an NGO.")
            return render(request, "login.html")

        login(request, user)
        messages.success(request, "Logged in successfully.")
        return redirect("dashboard")

    return render(request, "login.html")


# -------------------------
# NGO registration
# -------------------------
def NGOregistration(request):
    if request.method == "POST":
        ngo_name = request.POST.get("ngoname", "").strip()
        reg_no = request.POST.get("rno", "").strip()
        contact_person = request.POST.get("cperson", "").strip()
        address = request.POST.get("address", "").strip()
        phone = request.POST.get("phone", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")

        # Validate password match
        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return redirect("NGOregistration")

        # Prevent duplicate email
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("NGOregistration")

        # Create User (fullname must be NGO name!)
        user = User.objects.create_user(
            email=email,
            fullname=ngo_name,
            phone=phone,
            user_type="ngo",
            password=password
        )

        # Create NGO Profile
        NGOProfile.objects.create(
            user=user,
            ngo_name=ngo_name,
            registration_number=reg_no,
            contact_person=contact_person,
            address=address,
            phone=phone,
            email=email,
        )

        
        messages.success(request, "NGO registered successfully.please login")
        return redirect("NGOlogin")

    return render(request, "NGOregistration.html")

# -------------------------
# NGO login
# -------------------------
def NGOlogin(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)
        if user is None:
            messages.error(request, "Invalid email or password.")
            return render(request, "NGOlogin.html")

        # if user.user_type != "ngo":
        #     messages.error(request, "This login page is for NGOs only.")
        #     return render(request, "NGOlogin.html")

        login(request, user)
        messages.success(request, "Logged in as NGO.")
        return redirect("NGOdashboard")

    return render(request, "NGOlogin.html")


# -------------------------
# Logout
# -------------------------
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out.")
    return redirect("landing")


# -------------------------
# Dashboards
# -------------------------
@login_required(login_url='login')
@role_required(allowed_roles=['donor'], redirect_to='login')
def dashboard(request):
    # Add donor-specific context if needed
    return render(request, "dashboard.html")


@login_required(login_url='NGOlogin')
@role_required(allowed_roles=['ngo'], redirect_to='NGOlogin')
def NGOdashboard(request):
    # Add NGO-specific context if needed
    # e.g., profile = request.user.ngo_profile
    ctx = {}
    try:
        ctx['ngo_profile'] = request.user.ngo_profile
    except NGOProfile.DoesNotExist:
        ctx['ngo_profile'] = None
    return render(request, "NGOdashboard.html", ctx)


@login_required
def my_medicines(request):
    medicines = Medicine.objects.filter(donor=request.user).order_by('-id')
    return render(request, "my_medicines.html", {"medicines": medicines})


@login_required
def pickups(request):
    p = Pickup.objects.filter(donor=request.user)
    return render(request, "pickups.html", {"pickups": p})


@login_required
def ngo_requests(request):
    reqs = NGORequest.objects.filter(donor=request.user)
    return render(request, "ngo_requests.html", {"reqs": reqs})


@login_required
def settings(request):
    return render(request, "settings.html")


# add medicine view
@login_required
def add_medicine(request):
    if request.method == "POST":
        form = MedicineForm(request.POST)
        if form.is_valid():
            medicine = form.save(commit=False)
            medicine.donor = request.user
            medicine.save()
            return redirect("my_medicines")
    else:
        form = MedicineForm()

    return render(request, "add_medicine.html", {"form": form})