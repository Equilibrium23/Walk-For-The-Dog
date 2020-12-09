from django.shortcuts import render

def login(request):
    return render(request,'register_and_login/login.html') 

def register(request):
    return render(request,'register_and_login/register.html') 
