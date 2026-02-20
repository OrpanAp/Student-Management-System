from django.shortcuts import redirect
from django.contrib.auth.mixins import AccessMixin

class StaffRequiredMixin(AccessMixin):
    """
    Redirect non-staff users to home page
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated and not request.user.is_staff:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)
