from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from .models import User

def landing(request):
    return render(request,'landing.html') 
def home(request):
    return render(request,'login.html')
def registration(request):
    return render(request,'registration.html')
def dashboard(request):
    return render(request,'dashboard.html')

# Create your views here.
def NGOlogin(request):
    return render(request,'NGOlogin.html')

def NGOregistration(request):
    return render(request,'NGOregistration.html')   

def NGOdashboard(request):
    return render(request, 'NGOdashboard.html') 

User = get_user_model()

def register(request):
    if request.method == "POST":
        fullname = request.POST.get("fullname")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")

        # 1. Check password match
        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return render(request, "register.html")

        # 2. Check if email already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, "register.html")

        # 3. Create user
        user = User.objects.create_user(
            fullname=fullname,
            phone=phone,
            email=email,
            password=password
        )

        messages.success(request, "Account created successfully! You can now login.")
        return redirect("home")   # change to your login URL name

    return render(request, "register.html")

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Authenticate user
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect("dashboard")  # Change to your homepage/dashboard
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, "login.html")

    return render(request, "login.html")


