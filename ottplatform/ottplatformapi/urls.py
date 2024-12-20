from django.urls import path
from . import views

urlpatterns = [
    path('signupapi/', views.Ott_Signup,name='signup_api'),
    path('loginapi/', views.Login,name='login_api'),
    path('movielistapi/', views.List_Movie,name='movie_list'),
    path('movieviewapi/<int:id>/', views.movie_view,name='movie_view'),
    path('planlistapi/', views.List_Plan,name='plan_list'),

]