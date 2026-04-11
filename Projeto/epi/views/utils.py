from django.core.exceptions import ValidationError


def aplicar_erros_ao_form(exc, form):
    if hasattr(exc, "message_dict"):
        for field, errors in exc.message_dict.items():
            for error in errors:
                form.add_error(field if field in form.fields else None, error)
    else:
        form.add_error(None, exc.message)
