from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm 
from django.db import IntegrityError
# Create your views here

def SignupPage(request):
    if( request.method =='POST'):
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if  len(uname) == 0 or len(email) == 0 or len(pass1) == 0 or len(pass2) == 0 :
            return render(request,'signup.html',{'form':UserCreationForm(),'error':' Fields cannot be empty !'})

        if ( pass1 != pass2 ):
            return render(request,'signup.html',{'form':UserCreationForm(),'error':' Password mismatched !'})
        else:
            try:
                my_user = User.objects.create_user(uname,email,pass1)
                my_user.save() 
                return redirect('login')
            except IntegrityError:
                return render(request,'signup.html',{'form':UserCreationForm(),'error':' User Already Exist !'})

    
    return render(request,'signup.html')

def LoginPage(request):
    uname1 = request.POST.get('username')
    pass1 = request.POST.get('pass')
    
    if request.method == "POST":
        if  len(uname1) == 0 or len(pass1) == 0 :
            return render(request,'login.html',{'form':UserCreationForm(),'error':' Fields cannot be empty !'})
        user = None 
        if  (User.objects.filter(username = uname1).exists()):
            user = authenticate(username = uname1 , password = pass1)
        if ( user is None ):
            try :
                user = User.objects.get(email = uname1) 
                user = authenticate(username = user.username, password = pass1)
            except :
                return render(request,'login.html',{'form':UserCreationForm(),'error':' Wrong Credentials !'})
 
        if user is not None :
            login(request,user) 
            return redirect('home')
        else:
            return render(request,'login.html',{'form':UserCreationForm(),'error':' Wrong Credentials !'})
    return render(request,'login.html') 


def LogoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login') 
def HomePage(request):
    return render(request,'home.html') 
 
@login_required(login_url='login') 
def Profile(request):
    if(request.user.is_authenticated):
        return render( request, 'profile.html')
    else : 
        return redirect('/login') 

