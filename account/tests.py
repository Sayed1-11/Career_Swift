from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from account.models import UserProfile
from employee.models import Employee


class CandidateRegistrationTest(TestCase):
    """Candidate signs up via /registration/ → CANDIDATE role assigned."""

    def setUp(self):
        self.client = Client()
        self.url    = reverse('registration')

    def test_candidate_registration_creates_user_and_profile(self):
        data = {
            'first_name': 'Alice',
            'last_name':  'Seeker',
            'email':      'alice@test.com',
            'password1':  'SecurePass123!',
            'password2':  'SecurePass123!',
        }
        # The view sends an email – patch the backend so we don't need SMTP.
        with self.settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
            response = self.client.post(self.url, data)

        # Should redirect away (to login) now that the form is valid.
        self.assertIn(response.status_code, [200, 302])

        user = User.objects.filter(email='alice@test.com').first()
        self.assertIsNotNone(user, "User should be created after registration.")
        self.assertEqual(user.username, 'alice@test.com', "Username should equal email.")

        profile = UserProfile.objects.filter(user=user).first()
        self.assertIsNotNone(profile, "UserProfile should be created for the candidate.")
        self.assertEqual(profile.role, UserProfile.CANDIDATE)
        self.assertTrue(profile.is_candidate)
        self.assertFalse(profile.is_employer)


class EmployerRegistrationTest(TestCase):
    """Employer signs up via /register/ → Employee row + EMPLOYER role assigned."""

    def setUp(self):
        self.client = Client()
        self.url    = reverse('employee_register')

    def test_employer_registration_creates_user_employee_and_profile(self):
        data = {
            'first_name':     'Bob',
            'last_name':      'Employer',
            'email':          'bob@company.com',
            'password1':      'SecurePass123!',
            'password2':      'SecurePass123!',
            'company_name':   'Acme Corp',
            'company_mail':   'hr@acme.com',
            'company_number': '01700000000',
            'website':        'https://acme.com',
            'about':          'We build stuff.',
        }
        response = self.client.post(self.url, data)
        self.assertIn(response.status_code, [200, 302])

        user = User.objects.filter(email='bob@company.com').first()
        self.assertIsNotNone(user, "User should be created after employer registration.")

        employee = Employee.objects.filter(user=user).first()
        self.assertIsNotNone(employee, "Employee record should be created.")
        self.assertEqual(employee.company_name, 'Acme Corp')

        profile = UserProfile.objects.filter(user=user).first()
        self.assertIsNotNone(profile, "UserProfile should be created for the employer.")
        self.assertEqual(profile.role, UserProfile.EMPLOYER)
        self.assertTrue(profile.is_employer)
        self.assertFalse(profile.is_candidate)


class UserProfileModelTest(TestCase):
    """Unit-level tests for the UserProfile model itself."""

    def _make_user(self, email, role):
        user = User.objects.create_user(
            username=email, email=email, password='testpass'
        )
        profile = UserProfile.objects.create(user=user, role=role)
        return user, profile

    def test_candidate_properties(self):
        _, profile = self._make_user('c@test.com', UserProfile.CANDIDATE)
        self.assertTrue(profile.is_candidate)
        self.assertFalse(profile.is_employer)
        self.assertIn('Candidate', str(profile))

    def test_employer_properties(self):
        _, profile = self._make_user('e@test.com', UserProfile.EMPLOYER)
        self.assertTrue(profile.is_employer)
        self.assertFalse(profile.is_candidate)
        self.assertIn('Employer', str(profile))

    def test_default_role_is_candidate(self):
        user = User.objects.create_user(
            username='d@test.com', email='d@test.com', password='testpass'
        )
        profile = UserProfile.objects.create(user=user)
        self.assertEqual(profile.role, UserProfile.CANDIDATE)

    def test_deleting_user_deletes_profile(self):
        user, _ = self._make_user('del@test.com', UserProfile.CANDIDATE)
        user.delete()
        self.assertFalse(UserProfile.objects.filter(user__email='del@test.com').exists())


class LoginRedirectTest(TestCase):
    """Login should route candidates to home and employers to jobdetails."""

    def _create_active_user(self, email, role):
        user = User.objects.create_user(
            username=email, email=email, password='testpass', is_active=True
        )
        UserProfile.objects.create(user=user, role=role)
        return user

    def test_candidate_login_redirects_to_home(self):
        self._create_active_user('cand@test.com', UserProfile.CANDIDATE)
        response = self.client.post(reverse('login'), {
            'username': 'cand@test.com',
            'password': 'testpass',
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('home'), response['Location'])

    def test_employer_login_redirects_to_jobdetails(self):
        self._create_active_user('emp@test.com', UserProfile.EMPLOYER)
        response = self.client.post(reverse('login'), {
            'username': 'emp@test.com',
            'password': 'testpass',
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('jobdetails'), response['Location'])
