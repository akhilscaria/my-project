from django.shortcuts import redirect
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache

def api_login_required(view_func):
    @never_cache
    def wrapper(request, *args, **kwargs):
        if not request.session.get('is_authenticated'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper