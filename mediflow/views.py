from django.shortcuts import render
 
def home(request):
    return render(request,'login.html')
def registration(request):
    return render(request,'registration.html')
def dashboard(request):
    return render(request,'dashboard.html')

# Create your views here.
