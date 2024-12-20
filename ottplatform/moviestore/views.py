from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login,logout
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import AdminloginForm
from django.contrib import messages
from .models import MovieStore,Plan,AdminLogin,Subscribers,Watchhistory
from .forms import MovieModelForm,PlanForm,ForgotForm,ResetForm
from django.http import JsonResponse 
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.http import HttpResponse


def Adminlogin(request):
    if request.method == 'POST':
        form = AdminloginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
             auth_login(request, user)
             return redirect('moviestore')
        else:
            messages.error(request, 'incorrect email or password!')
    else:
        form = AdminloginForm()
    return render(request, 'login.html', {'form': form})
  



def forget_pass(request):
    message = None
    if request.method == 'POST':
        form = ForgotForm(data=request.POST)  
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if AdminLogin.objects.filter(email=email).exists():
                user = AdminLogin.objects.get(email=email)
                token = get_random_string(length=32)
                user.forgotkey = token
                user.save()
                subject = "Click the link below to reset your password:"
                from_email = "babudeepu7@gmail.com"
                recipient_list = [email]
                message = "http://127.0.0.1:8000/reset/" + token + "/" 
                send_mail(subject, message, from_email, recipient_list, fail_silently=True)
                message = {'status': 'Check your Email'}
            else:
                message = {'status': 'User with this email does not exist'}
    else:
        form = ForgotForm()
    
    return render(request, 'forgetpass.html', {'message': message, 'form': form})


def reset_pass(request , key):
    if AdminLogin.objects.filter(forgotkey = key).exists():
        user = AdminLogin.objects.get(forgotkey = key)
        form = ResetForm(request.POST)
        if form.is_valid():
            pass1 = form.cleaned_data.get('password')
            pass2 = form.cleaned_data.get('confrimpassword')
            if pass1 == pass2:
                user.password = make_password(pass1)
                user.forgotkey=None
                user.save()
                return redirect ('adminlogin')
            else:
                message = {'status': 'Password doesnot match,try again'}
        else:
            form = ResetForm() 
    else:    
       return redirect('adminlogin')               
    return render(request, 'resetpass.html',{'message' : message})


def Admin_logout(request):
    if request.method == 'POST':  
        logout(request)
        return redirect('adminlogin')  
    context = {
        'user': request.user
    }
    return render(request, 'logout.html' , context)


def movie_store(request):
     Movie_list = MovieStore.objects.all()
     paginator = Paginator(Movie_list,2)
     page_number = request.GET.get('page')
     try:
         Movie_list = paginator.page(page_number)
     except PageNotAnInteger:
         Movie_list = paginator.page(1)
     except EmptyPage:
         Movie_list = paginator.page(paginator.num_pages)
     return render(request,'moviestore.html',{'Movie_list':Movie_list})



def add_movie(request):
    if request.method == 'POST':
        form = MovieModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('moviestore') # Redirect to the movie list page after successful submission
    else:
        form = MovieModelForm()
    return render(request, 'addmovie.html', {'form': form})
    
    

def movie_details(request , id):
    movieview = get_object_or_404(MovieStore, pk=id)
    return render(request, 'views.html', {'movieview':movieview})


def edit_movie(request, id):
    movie = MovieStore.objects.get(pk=id)
    if request.method == 'POST':
        form = MovieModelForm(request.POST,request.FILES,instance=movie)
        if form.is_valid():
            form.save()
            return redirect('moviestore')
    else:
        form =MovieModelForm(instance=movie)           
    return render(request, 'edit.html', {'form': form})

def delete_movie(request,id):
    movie = get_object_or_404(MovieStore, pk=id)
    if request.method == 'POST':
        movie.delete()
        return redirect('moviestore')  # Redirect to the page listing movies
    return render(request, 'moviestore.html', {'movie': movie})


def subscription_plan(request):
    plan_list = Plan.objects.all()
    return render(request, 'subscrptionplan.html', {'planlist': plan_list})



def plan_views(request, id):
    planview = get_object_or_404(Plan, pk=id)
    return render(request, 'planviews.html', {'planview':planview})


def add_plan(request):
    if request.method == 'POST':
        form = PlanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subplan') # Redirect to the movie list page after successful submission
    else:
        form = PlanForm()
    return render(request, 'addplan.html', {'form': form})


def usermanage_list(request):
      user_list = AdminLogin.objects.filter(is_staff = 0)
      return render(request, 'usermanagelist.html', {'user_list': user_list})



def usermanage_details(request, id):
    subscribers_list = Subscribers.objects.filter(userid=id)
    watch_history = Watchhistory.objects.filter(userid = id)
    return render(request, 'usermanagehistory.html', {'subscribers': subscribers_list , 'watchhistory' : watch_history})


def revenue_page(request):
    return render(request, 'revenue.html')


def most_viewed(request):
    return render(request, 'mostviewed.html')


def highest_rated(request):
    return render(request, 'highestrated.html')


# def subscribers_count(request):
#     return render(request, 'subscribers.html')


def search_movie(request):
    query = request.GET.get('q', '')
    if query:
        movie =  MovieStore.objects.filter(title__icontains=query) |  MovieStore.objects.filter(url__icontains=query)
    else:
        movie =  MovieStore.objects.all()

    # Prepare the data to send in the response
    movie_list = list(movie.values('id','moviename', 'rating', 'thumpnail','action'))
    return JsonResponse(movie_list, safe=False)


def plantoggle(request , pk):
    plan = get_object_or_404(Plan , pk=pk)
    if request.method == 'POST':
        if plan.status == 'true':
            plan.status = 'false'
            plan.save()
        else:
            plan.status = 'true'
            plan.save()
    else:
        return redirect ('subplan') 
    return redirect ('subplan') 
         
     











