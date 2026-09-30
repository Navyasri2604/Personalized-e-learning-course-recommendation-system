from django.contrib import admin
from .models import UserProfile, Course, SavedCourse, LearningProgress

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'full_name', 'career_goal')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'category', 'difficulty', 'rating')
    search_fields = ('course_name', 'category', 'skills')
    list_filter = ('category', 'difficulty')

@admin.register(SavedCourse)
class SavedCourseAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'saved_at')

@admin.register(LearningProgress)
class LearningProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'status', 'updated_at')
    list_filter = ('status',)
