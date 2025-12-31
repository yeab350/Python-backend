from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Require an authenticated staff user (admin-only UI)."""

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.is_staff
