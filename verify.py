import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elearning_system.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from recommender.models import Course, UserProfile, SavedCourse, LearningProgress
from recommender.recommendation_engine import get_recommendations
from recommender.roadmap_generator import generate_roadmap

print('=== DB Stats ===')
print('Courses:', Course.objects.count())
print('Users:', UserProfile.objects.count())
print('Saved:', SavedCourse.objects.count())
print('Progress:', LearningProgress.objects.count())

cats = Course.objects.values_list('category', flat=True).distinct()
print('\n=== Categories ===')
for c in cats[:10]:
    print(' -', c)

user = UserProfile.objects.first()
if user:
    user.interests = 'Python Machine Learning AI'
    user.career_goal = 'Data Scientist'
    recs = get_recommendations(user)
    print('\n=== Recommendation Engine (TF-IDF + Cosine Sim) ===')
    print('User:', user.username)
    print('Returned', len(recs), 'recommendations')
    for r in recs[:3]:
        print('  -', r.course_name)
else:
    print('No users found in DB')

print('\n=== Roadmap Generator ===')
roadmap = generate_roadmap('AI Engineer')
print('Roadmap steps for AI Engineer:', len(roadmap))
for step in roadmap[:3]:
    print('  Step', step['step'], '-', step['title'])

print('\n=== URL Check ===')
from django.test import Client
c = Client()
urls_to_check = [
    ('Home', '/'),
    ('Login', '/login/'),
    ('Register', '/register/'),
]
for name, url in urls_to_check:
    response = c.get(url)
    print(f'  {name} ({url}): HTTP {response.status_code}')

print('\n=== Auth-Protected URL Redirects ===')
protected = [
    ('Dashboard', '/dashboard/'),
    ('Courses', '/courses/'),
    ('Recommendations', '/recommendations/'),
    ('Roadmap', '/roadmap/'),
    ('Analytics', '/analytics/'),
    ('Profile', '/profile/'),
    ('Saved Courses', '/saved-courses/'),
]
for name, url in protected:
    response = c.get(url)
    print(f'  {name} ({url}): HTTP {response.status_code} (should redirect to login)')

print('\n=== Authenticated Requests ===')
from recommender.models import UserProfile
test_users = UserProfile.objects.filter(is_superuser=True)
if test_users.exists():
    su = test_users.first()
    c.force_login(su)
    auth_urls = [
        ('Dashboard', '/dashboard/'),
        ('Courses', '/courses/'),
        ('Recommendations', '/recommendations/'),
        ('Roadmap', '/roadmap/'),
        ('Analytics', '/analytics/'),
        ('Profile', '/profile/'),
        ('Saved Courses', '/saved-courses/'),
    ]
    for name, url in auth_urls:
        try:
            response = c.get(url)
            print(f'  {name} ({url}): HTTP {response.status_code}')
        except Exception as e:
            print(f'  {name} ({url}): ERROR - {e}')
    
    # Test first course
    first_course = Course.objects.first()
    if first_course:
        resp = c.get(f'/course/{first_course.pk}/')
        print(f'  Course Detail (/course/{first_course.pk}/): HTTP {resp.status_code}')
        resp2 = c.get(f'/course/{first_course.pk}/enroll/')
        print(f'  Enroll Page (/course/{first_course.pk}/enroll/): HTTP {resp2.status_code}')
else:
    print('  No superuser found. Skipping authenticated tests.')

print('\nAll checks complete!')
