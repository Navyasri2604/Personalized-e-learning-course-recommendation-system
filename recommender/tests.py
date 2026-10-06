from django.test import TestCase, Client
from django.urls import reverse
from .models import UserProfile, Course, SavedCourse, LearningProgress
from .recommendation_engine import get_recommendations
from .roadmap_generator import generate_roadmap


def create_test_user(username='testuser', password='TestPass123!'):
    """Helper: create a test user."""
    user = UserProfile.objects.create_user(
        username=username,
        password=password,
        email=f'{username}@test.com',
        full_name='Test User'
    )
    return user


def create_test_course(name='Test Course', category='Programming', difficulty='Beginner'):
    """Helper: create a test course."""
    return Course.objects.create(
        course_name=name,
        university='Test University',
        category=category,
        difficulty=difficulty,
        rating=4.5,
        duration='10 hours',
        description='A test course about testing things.',
        skills='Python Testing Django',
        course_url='https://example-course.com/test'
    )


# ─────────────────────────────────────────────
# 1. Authentication Tests
# ─────────────────────────────────────────────
class AuthenticationTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = create_test_user()

    def test_home_page_unauthenticated(self):
        """Home page should render for unauthenticated users."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_page_redirects_authenticated(self):
        """Home page should redirect authenticated users to dashboard."""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('dashboard'))

    def test_register_get(self):
        """Register page should return 200."""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_register_post_success(self):
        """Registration should succeed with valid data."""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@test.com',
            'full_name': 'New User',
            'password1': 'StrongPass99!',
            'password2': 'StrongPass99!'
        })
        self.assertEqual(UserProfile.objects.filter(username='newuser').count(), 1)

    def test_login_get(self):
        """Login page should return 200."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_post_valid(self):
        """Login with valid credentials should redirect to dashboard."""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'TestPass123!'
        })
        self.assertRedirects(response, reverse('dashboard'))

    def test_login_post_invalid(self):
        """Login with wrong password should stay on login page."""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)

    def test_login_preserves_next_param(self):
        """Login should redirect to ?next= URL after success."""
        response = self.client.post(
            reverse('login') + '?next=/courses/',
            {'username': 'testuser', 'password': 'TestPass123!', 'next': '/courses/'}
        )
        self.assertRedirects(response, '/courses/')

    def test_logout(self):
        """Logout should redirect to home."""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('home'))


# ─────────────────────────────────────────────
# 2. Authentication Protection Tests
# ─────────────────────────────────────────────
class AuthProtectionTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response['Location'])

    def test_courses_requires_login(self):
        response = self.client.get(reverse('course_list'))
        self.assertEqual(response.status_code, 302)

    def test_recommendations_requires_login(self):
        response = self.client.get(reverse('recommendations'))
        self.assertEqual(response.status_code, 302)

    def test_roadmap_requires_login(self):
        response = self.client.get(reverse('roadmap'))
        self.assertEqual(response.status_code, 302)

    def test_analytics_requires_login(self):
        response = self.client.get(reverse('analytics'))
        self.assertEqual(response.status_code, 302)

    def test_profile_requires_login(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)

    def test_saved_courses_requires_login(self):
        response = self.client.get(reverse('saved_courses'))
        self.assertEqual(response.status_code, 302)

    def test_enroll_requires_login(self):
        course = create_test_course()
        response = self.client.get(reverse('enroll_course', args=[course.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response['Location'])


# ─────────────────────────────────────────────
# 3. Course Tests
# ─────────────────────────────────────────────
class CourseTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = create_test_user()
        self.course = create_test_course()
        self.client.login(username='testuser', password='TestPass123!')

    def test_course_list_renders(self):
        response = self.client.get(reverse('course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Course')

    def test_course_search(self):
        response = self.client.get(reverse('course_list') + '?q=Test')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Course')

    def test_course_search_no_results(self):
        response = self.client.get(reverse('course_list') + '?q=zzznomatch')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No courses found')

    def test_course_detail_renders(self):
        response = self.client.get(reverse('course_detail', args=[self.course.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Course')
        self.assertContains(response, 'Enroll Now')

    def test_course_detail_404(self):
        response = self.client.get(reverse('course_detail', args=[99999]))
        self.assertEqual(response.status_code, 404)


# ─────────────────────────────────────────────
# 4. Enrollment Flow Tests
# ─────────────────────────────────────────────
class EnrollmentTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = create_test_user()
        self.course = create_test_course()
        self.client.login(username='testuser', password='TestPass123!')

    def test_enrollment_page_renders(self):
        response = self.client.get(reverse('enroll_course', args=[self.course.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Confirm Enrollment')

    def test_process_enrollment_creates_progress(self):
        response = self.client.post(reverse('process_enrollment', args=[self.course.pk]))
        self.assertTrue(
            LearningProgress.objects.filter(user=self.user, course=self.course).exists()
        )
        progress = LearningProgress.objects.get(user=self.user, course=self.course)
        self.assertEqual(progress.status, 'Started')

    def test_process_enrollment_redirects_to_learn(self):
        response = self.client.post(reverse('process_enrollment', args=[self.course.pk]))
        self.assertRedirects(response, reverse('course_learn', args=[self.course.pk]))

    def test_already_enrolled_redirects_to_learn(self):
        LearningProgress.objects.create(user=self.user, course=self.course, status='Started')
        response = self.client.get(reverse('enroll_course', args=[self.course.pk]))
        self.assertRedirects(response, reverse('course_learn', args=[self.course.pk]))

    def test_course_learn_page_renders(self):
        LearningProgress.objects.create(user=self.user, course=self.course, status='Started')
        response = self.client.get(reverse('course_learn', args=[self.course.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Course')

    def test_course_learn_requires_enrollment(self):
        response = self.client.get(reverse('course_learn', args=[self.course.pk]))
        self.assertRedirects(response, reverse('enroll_course', args=[self.course.pk]))


# ─────────────────────────────────────────────
# 5. Save/Unsave Tests
# ─────────────────────────────────────────────
class SaveCourseTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = create_test_user()
        self.course = create_test_course()
        self.client.login(username='testuser', password='TestPass123!')

    def test_save_course(self):
        self.client.get(reverse('save_course', args=[self.course.pk]))
        self.assertTrue(SavedCourse.objects.filter(user=self.user, course=self.course).exists())

    def test_remove_saved_course(self):
        SavedCourse.objects.create(user=self.user, course=self.course)
        self.client.get(reverse('remove_saved_course', args=[self.course.pk]))
        self.assertFalse(SavedCourse.objects.filter(user=self.user, course=self.course).exists())

    def test_saved_courses_page(self):
        SavedCourse.objects.create(user=self.user, course=self.course)
        response = self.client.get(reverse('saved_courses'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Course')


# ─────────────────────────────────────────────
# 6. Progress Update Tests
# ─────────────────────────────────────────────
class ProgressTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = create_test_user()
        self.course = create_test_course()
        self.client.login(username='testuser', password='TestPass123!')

    def test_update_progress_started(self):
        self.client.post(reverse('update_progress', args=[self.course.pk]), {'status': 'Started'})
        p = LearningProgress.objects.get(user=self.user, course=self.course)
        self.assertEqual(p.status, 'Started')

    def test_update_progress_completed(self):
        self.client.post(reverse('update_progress', args=[self.course.pk]), {'status': 'Completed'})
        p = LearningProgress.objects.get(user=self.user, course=self.course)
        self.assertEqual(p.status, 'Completed')

    def test_update_progress_invalid_status(self):
        """Invalid status should not be saved."""
        self.client.post(reverse('update_progress', args=[self.course.pk]), {'status': 'INVALID'})
        self.assertFalse(LearningProgress.objects.filter(user=self.user, course=self.course).exists())


# ─────────────────────────────────────────────
# 7. Profile Tests
# ─────────────────────────────────────────────
class ProfileTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = create_test_user()
        self.client.login(username='testuser', password='TestPass123!')

    def test_profile_page_renders(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_profile_update(self):
        response = self.client.post(reverse('profile'), {
            'full_name': 'Updated Name',
            'email': 'updated@test.com',
            'interests': 'AI Python',
            'skills': 'Django REST',
            'career_goal': 'AI Engineer'
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.career_goal, 'AI Engineer')


# ─────────────────────────────────────────────
# 8. Dashboard Tests
# ─────────────────────────────────────────────
class DashboardTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = create_test_user()
        self.client.login(username='testuser', password='TestPass123!')

    def test_dashboard_renders(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')

    def test_dashboard_shows_stats(self):
        course = create_test_course()
        SavedCourse.objects.create(user=self.user, course=course)
        LearningProgress.objects.create(user=self.user, course=course, status='Completed')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)


# ─────────────────────────────────────────────
# 9. Recommendation Engine Tests
# ─────────────────────────────────────────────
class RecommendationTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = create_test_user()
        self.client.login(username='testuser', password='TestPass123!')
        for i in range(5):
            create_test_course(name=f'Python Course {i}', category='Programming')

    def test_recommendations_page_renders(self):
        response = self.client.get(reverse('recommendations'))
        self.assertEqual(response.status_code, 200)

    def test_engine_returns_results_with_no_profile(self):
        """Should return highest rated when no profile (returns QuerySet or list)."""
        recs = get_recommendations(self.user)
        # Engine returns QuerySet (no profile) or list (with profile) — both are iterable
        self.assertTrue(hasattr(recs, '__iter__'), "Result should be iterable")
        self.assertGreater(len(list(recs)), 0, "Should have at least 1 result")

    def test_engine_returns_results_with_profile(self):
        self.user.interests = 'Python Django'
        self.user.career_goal = 'Web Developer'
        recs = get_recommendations(self.user)
        self.assertGreater(len(list(recs)), 0)


# ─────────────────────────────────────────────
# 10. Roadmap Tests
# ─────────────────────────────────────────────
class RoadmapTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = create_test_user()
        self.client.login(username='testuser', password='TestPass123!')

    def test_roadmap_page_no_goal(self):
        """Roadmap with no career goal should show prompt."""
        response = self.client.get(reverse('roadmap'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No Career Goal Set')

    def test_roadmap_page_with_goal(self):
        self.user.career_goal = 'AI Engineer'
        self.user.save()
        response = self.client.get(reverse('roadmap'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'AI Engineer')

    def test_roadmap_generator_known_goal(self):
        steps = generate_roadmap('AI Engineer')
        self.assertGreater(len(steps), 0)
        self.assertIn('title', steps[0])
        self.assertIn('step', steps[0])

    def test_roadmap_generator_unknown_goal(self):
        steps = generate_roadmap('ZZZ Unknown Goal XYZ')
        self.assertIsInstance(steps, list)


# ─────────────────────────────────────────────
# 11. Analytics Tests
# ─────────────────────────────────────────────
class AnalyticsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = create_test_user()
        self.client.login(username='testuser', password='TestPass123!')

    def test_analytics_page_renders(self):
        response = self.client.get(reverse('analytics'))
        self.assertEqual(response.status_code, 200)

    def test_analytics_with_progress_data(self):
        course = create_test_course()
        LearningProgress.objects.create(user=self.user, course=course, status='Completed')
        response = self.client.get(reverse('analytics'))
        self.assertEqual(response.status_code, 200)


# ─────────────────────────────────────────────
# 12. CSRF Tests
# ─────────────────────────────────────────────
class CSRFTests(TestCase):

    def setUp(self):
        self.user = create_test_user()

    def test_login_form_has_csrf(self):
        response = self.client.get(reverse('login'))
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_register_form_has_csrf(self):
        response = self.client.get(reverse('register'))
        self.assertContains(response, 'csrfmiddlewaretoken')
