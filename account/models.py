from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Extends the built-in User with a role so every registered
    user is explicitly a CANDIDATE or an EMPLOYER from sign-up.
    """
    CANDIDATE = 'candidate'
    EMPLOYER  = 'employer'
    ROLE_CHOICES = [
        (CANDIDATE, 'Candidate'),
        (EMPLOYER,  'Employer'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=CANDIDATE,
    )

    class Meta:
        verbose_name        = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"{self.user.email} ({self.get_role_display()})"

    # ── convenience helpers ─────────────────────────────────────────────────

    @property
    def is_candidate(self):
        return self.role == self.CANDIDATE

    @property
    def is_employer(self):
        return self.role == self.EMPLOYER
