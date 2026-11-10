from django.shortcuts import render


def inicio(request):
    return render(request, 'core/inicio.html')


def acceso_denegado(request):
    return render(request, 'core/acceso_denegado.html', status=403)