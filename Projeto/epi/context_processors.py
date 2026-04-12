def perfil_usuario(request):
    if not request.user.is_authenticated:
        return {"pode_operar": False}
    if request.user.is_superuser:
        return {"pode_operar": True}
    grupos = set(request.user.groups.values_list("name", flat=True))
    return {"pode_operar": bool(grupos & {"Administrador", "Almoxarife"})}
