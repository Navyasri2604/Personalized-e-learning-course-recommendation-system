from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    
    path('courses/', views.course_list, name='course_list'),
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
    path('course/<int:pk>/enroll/', views.enroll_course, name='enroll_course'),
    path('course/<int:pk>/enroll/process/', views.process_enrollment, name='process_enrollment'),
    path('course/<int:pk>/learn/', views.course_learn, name='course_learn'),
    path('course/<int:pk>/save/', views.save_course, name='save_course'),
    path('course/<int:pk>/remove/', views.remove_saved_course, name='remove_saved_course'),
    path('course/<int:pk>/progress/', views.update_progress, name='update_progress'),
    
    path('saved-courses/', views.saved_courses, name='saved_courses'),
    path('recommendations/', views.recommendations_view, name='recommendations'),
    path('roadmap/', views.roadmap_view, name='roadmap'),
    path('analytics/', views.analytics_view, name='analytics'),
]
