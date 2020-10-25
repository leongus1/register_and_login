from django.shortcuts import render, redirect
from . models import Users
from django.contrib import messages
import bcrypt

# Create your views here.

###---RENDER
def index(request):
    return render(request, 'index.html')

def login(request):
    try:
        request.session['login']
    except:
        return redirect('/')
    else:   
        print('successful log in')
        return render(request, 'logged_in.html')

###---REDIRECT
def success_login(request):
    if request.method == "GET":
        print("a GET request came in")
        return redirect ('/')
    else:
        print('a POST request came in')
        return redirect('/register/success/')


###---DATA PROCESSING
def register(request):
    errors = Users.objects.user_validator(request.POST)
    print (errors)
    if len(Users.objects.filter(email=request.POST['email']))>0:
        errors['dupicate_account'] = "There is already an account with this email address. Please try to log in."
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect ('/')
    else:
        Users.objects.create(first_name = request.POST['first_name'], last_name=request.POST['last_name'], birthdate=request.POST['birthdate'],email=request.POST['email'], password_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode())
        request.session['name']=request.POST['first_name']
        request.session['login']= True
        return redirect ('success/')
    
    
def log_check(request):
    request.session.flush()
    user = Users.objects.filter(email=request.POST['email'])
    if len(user)>0:
        logged_user=user[0]
        if bcrypt.checkpw(request.POST['pw'].encode(), logged_user.password_hash.encode()):
            print('Passwords match')
            request.session['name'] = logged_user.first_name
            request.session['login']=True
            return redirect ('/register/success/')
        else:
            print('Password does NOT match!')
            request.session['bad_pw'] = "Invalid Password. Try again!"
            return redirect ('/')
    else:
        request.session['invalid_user_email'] = "Invalid User Email Address!!!"
        return redirect('/')
     
def logout(request):
    request.session.flush()
    return redirect('/')
    