
from django.contrib import admin
from django.urls import path,include
from moviestore import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.Adminlogin,name='adminlogin'),
    path('forgetpwd', views.forget_pass,name='forgotpass'),
    path('resetpwd/<str:key>/', views.reset_pass,name="reset"),
    path('logout', views.Admin_logout, name='adminlogout'),
    path('movie', views.movie_store, name ='moviestore'),
    path('addmovie', views.add_movie, name ='addmovie'),
    path('details/<int:id>/', views.movie_details, name='moviedetails'),
    path('editmovie/<int:id>/', views.edit_movie, name='editmovie'),
    path('plan', views.subscription_plan,name='subplan'),
    path('planviews/<int:id>/', views.plan_views, name='planview'),
    path('addplan', views.add_plan, name='addplan'),
    path('usermanagelist', views.usermanage_list, name='userlist'),
    path('usermanagedetails/<int:id>/', views.usermanage_details,name='userdetails'),
    path('revenue', views.revenue_page),
    path('mostviewed', views.most_viewed),
    path('highestrated', views.highest_rated),
    # path('subscriberscount', views.subscribers_count),
    path('deletemovie/<int:id>/', views.delete_movie, name='deletemovie'),
    path('search', views.search_movie, name='searchmovie'),
    path('ottplatformapi/', include('ottplatformapi.urls')),
     path('plantoggle/<int:pk>/', views.plantoggle, name = 'plantoggle'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)


