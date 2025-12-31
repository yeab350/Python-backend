from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render


def _is_staff(user):
    return user.is_authenticated and user.is_staff


def staff_required(view_func):
    return login_required(user_passes_test(_is_staff)(view_func))


@staff_required
def dashboard(request):
    return render(request, "staff/dashboard.html")
