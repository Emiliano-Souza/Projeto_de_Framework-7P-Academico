from functools import wraps

from django.core.exceptions import ValidationError
from django.shortcuts import render


def aplicar_erros_ao_form(exc, form):
    if hasattr(exc, "message_dict"):
        for field, errors in exc.message_dict.items():
            for error in errors:
                form.add_error(field if field in form.fields else None, error)
    else:
        form.add_error(None, exc.message)


def grupo_required(*grupos):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                from django.contrib.auth.views import redirect_to_login
                return redirect_to_login(request.get_full_path())
            if request.user.is_superuser or request.user.groups.filter(name__in=grupos).exists():
                return view_func(request, *args, **kwargs)
            return render(request, "epi/acesso_negado.html", status=403)
        return wrapper
    return decorator
