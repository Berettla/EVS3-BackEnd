from django.shortcuts import render
from apps.catalogo.models import Producto


def inicio(request):
    destacados = (
        Producto.objects.filter(activo=True, destacado=True)
        .select_related('categoria')[:4]
    )
    return render(request, 'core/inicio.html', {'destacados': destacados})


def acceso_denegado(request):
    return render(request, 'core/acceso_denegado.html', status=403)