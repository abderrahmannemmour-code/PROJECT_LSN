"""Middleware to track last_seen timestamp for authenticated students."""
from django.utils import timezone


class UpdateLastSeenMiddleware:
    """
    Updates Student.last_seen every time an authenticated student makes a request.
    Runs after authentication so request.user is available.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Only update for authenticated students (do it after response to not slow down request)
        if request.user and request.user.is_authenticated:
            try:
                from core.models import Student
                if hasattr(request.user, 'role') and request.user.role == 'student':
                    Student.objects.filter(pk=request.user.pk).update(last_seen=timezone.now())
            except Exception:
                pass  # Never crash a request just because of this

        return response
