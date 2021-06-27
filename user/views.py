from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
def sign_in(request):
    return render(request, 'registration.html')

def log_in(request):
    return render(request, 'login.html')


