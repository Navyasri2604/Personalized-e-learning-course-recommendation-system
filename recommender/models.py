from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    interests = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    career_goal = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username

class Course(models.fields.Model if hasattr(models.fields, 'Model') else models.Model):
    course_name = models.CharField(max_length=500)
    university = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=50, choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')])
    rating = models.FloatField(default=0.0)
    duration = models.CharField(max_length=100)
    description = models.TextField()
    skills = models.TextField()
    course_url = models.URLField(max_length=500)

    def __str__(self):
        return self.course_name

class SavedCourse(models.fields.Model if hasattr(models.fields, 'Model') else models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='saved_courses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user.username} - {self.course.course_name}"

class LearningProgress(models.fields.Model if hasattr(models.fields, 'Model') else models.Model):
    STATUS_CHOICES = [
        ('Started', 'Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='progress')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Started')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user.username} - {self.course.course_name} ({self.status})"
