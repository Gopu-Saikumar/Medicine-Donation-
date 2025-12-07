from django.shortcuts import render

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
