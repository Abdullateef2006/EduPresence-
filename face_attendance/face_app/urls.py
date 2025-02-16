from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.sign_up, name='signup'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
     path('live-feed/', views.live_feed, name='live_feed'),
    path('video-feed/', views.video_feed, name='video_feed'), 
        path('dash/', views.dash, name='dash'), 
            path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path('check-attendance-status/', views.check_attendance_status, name='check_status'),

]
