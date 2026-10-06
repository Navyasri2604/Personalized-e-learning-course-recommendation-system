from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .models import Course, SavedCourse, LearningProgress
from .forms import CustomUserCreationForm, UserProfileForm
from .recommendation_engine import get_recommendations
from .roadmap_generator import generate_roadmap

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'recommender/home.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful. Please complete your profile.")
            next_url = request.POST.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('profile')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = CustomUserCreationForm()
    return render(request, 'recommender/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.POST.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'recommender/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    total_courses = Course.objects.count()
    saved_count = SavedCourse.objects.filter(user=request.user).count()
    progress_count = LearningProgress.objects.filter(user=request.user, status='Completed').count()
    
    recommendations = get_recommendations(request.user)
    
    context = {
        'total_courses': total_courses,
        'saved_count': saved_count,
        'progress_count': progress_count,
        'recommendations': recommendations[:4], # Show top 4 on dashboard
    }
    return render(request, 'recommender/dashboard.html', context)

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'recommender/profile.html', {'form': form})

@login_required
def recommendations_view(request):
    recommendations = get_recommendations(request.user)
    return render(request, 'recommender/recommendations.html', {'courses': recommendations})

@login_required
def roadmap_view(request):
    goal = request.user.career_goal
    roadmap = generate_roadmap(goal) if goal else []
    return render(request, 'recommender/roadmap.html', {'roadmap': roadmap, 'goal': goal})

@login_required
def course_list(request):
    query = request.GET.get('q', '')
    if query:
        courses = Course.objects.filter(course_name__icontains=query) | Course.objects.filter(category__icontains=query) | Course.objects.filter(skills__icontains=query)
    else:
        courses = Course.objects.all()[:50] # Limit to 50 for performance
    return render(request, 'recommender/course_list.html', {'courses': courses, 'query': query})

@login_required
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    is_saved = SavedCourse.objects.filter(user=request.user, course=course).exists()
    
    progress = LearningProgress.objects.filter(user=request.user, course=course).first()
    status = progress.status if progress else None
        
    return render(request, 'recommender/course_detail.html', {'course': course, 'is_saved': is_saved, 'status': status})

@login_required
def save_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    SavedCourse.objects.get_or_create(user=request.user, course=course)
    messages.success(request, f'"{course.course_name}" has been saved.')
    return redirect('course_detail', pk=pk)

@login_required
def remove_saved_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    SavedCourse.objects.filter(user=request.user, course=course).delete()
    messages.success(request, f'"{course.course_name}" removed from saved courses.')
    return redirect('saved_courses')

@login_required
def saved_courses(request):
    saved = SavedCourse.objects.filter(user=request.user).select_related('course')
    return render(request, 'recommender/saved_courses.html', {'saved': saved})

@login_required
def update_progress(request, pk):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=pk)
        status = request.POST.get('status')
        if status in ['Started', 'In Progress', 'Completed']:
            progress, created = LearningProgress.objects.get_or_create(user=request.user, course=course)
            progress.status = status
            progress.save()
            messages.success(request, f'Progress updated to {status}.')
    return redirect('course_detail', pk=pk)

@login_required
def analytics_view(request):
    category_data = Course.objects.values('category').annotate(count=Count('id'))
    categories = [item['category'] for item in category_data]
    counts = [item['count'] for item in category_data]
    
    progress_data = LearningProgress.objects.filter(user=request.user).values('status').annotate(count=Count('id'))
    prog_labels = [item['status'] for item in progress_data]
    prog_counts = [item['count'] for item in progress_data]
    
    return render(request, 'recommender/analytics.html', {
        'categories': categories,
        'counts': counts,
        'prog_labels': prog_labels,
        'prog_counts': prog_counts
    })

@login_required(login_url='/login/')
def enroll_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    # Check if already enrolled
    enrolled = LearningProgress.objects.filter(user=request.user, course=course).exists()
    if enrolled:
        return redirect('course_learn', pk=pk)
        
    return render(request, 'recommender/enrollment.html', {'course': course})

@login_required(login_url='/login/')
def process_enrollment(request, pk):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=pk)
        LearningProgress.objects.get_or_create(
            user=request.user,
            course=course,
            defaults={'status': 'Started'}
        )
        messages.success(request, f"Successfully enrolled in {course.course_name}!")
        return redirect('course_learn', pk=pk)
    return redirect('course_detail', pk=pk)

@login_required(login_url='/login/')
def course_learn(request, pk):
    course = get_object_or_404(Course, pk=pk)
    # Ensure they are enrolled
    try:
        progress = LearningProgress.objects.get(user=request.user, course=course)
    except LearningProgress.DoesNotExist:
        messages.error(request, "You must enroll in this course to view its content.")
        return redirect('enroll_course', pk=pk)
        
    return render(request, 'recommender/course_learn.html', {
        'course': course,
        'progress': progress
    })
