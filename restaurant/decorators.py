from functools import wraps
from django.shortcuts import redirect

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.session.get('user_type') != 'admin':
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
