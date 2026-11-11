from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from apps.catalogo.models import Producto

from .cotizacion import Cotizacion, CotizacionError


def ver_cotizacion(request):
    cotizacion = Cotizacion(request)
    lineas = cotizacion.lineas()
    return render(request, 'cotizador/cotizacion.html', {
        'lineas': lineas,
        'totales': cotizacion.totales(lineas),
    })


@require_POST
def agregar(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, activo=True)
    cotizacion = Cotizacion(request)
    try:
        cantidad = int(request.POST.get('cantidad', ''))
        cotizacion.agregar(producto, cantidad)
        messages.success(request, f'Agregaste {cantidad} × "{producto.nombre}" a tu cotización.')
    except ValueError:
        messages.error(request, 'Ingresa una cantidad válida.')
    except CotizacionError as error:
        messages.error(request, str(error))

    # Vuelve a la ficha conservando los filtros del catálogo
    destino = reverse('catalogo:detalle', args=[producto.slug])
    filtros = request.POST.get('qs', '')
    return redirect(f'{destino}?{filtros}' if filtros else destino)


@require_POST
def actualizar(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    cotizacion = Cotizacion(request)
    try:
        cantidad = int(request.POST.get('cantidad', ''))
        cotizacion.actualizar(producto, cantidad)
        messages.success(request, 'Cantidad actualizada.')
    except ValueError:
        messages.error(request, 'Ingresa una cantidad válida.')
    except CotizacionError as error:
        messages.error(request, str(error))
    return redirect('cotizador:ver')


@require_POST
def quitar(request, producto_id):
    Cotizacion(request).quitar(producto_id)
    messages.success(request, 'Producto quitado de tu cotización.')
    return redirect('cotizador:ver')


@require_POST
def vaciar(request):
    Cotizacion(request).vaciar()
    messages.success(request, 'Tu cotización quedó vacía.')
    return redirect('cotizador:ver')


@login_required
@require_POST
def confirmar(request):
    cotizacion = Cotizacion(request)
    if not len(cotizacion):
        messages.warning(request, 'Tu cotización está vacía.')
        return redirect('catalogo:lista')

    lineas = cotizacion.lineas()
    errores = cotizacion.errores_disponibilidad(lineas)
    if errores:
        for error in errores:
            messages.error(request, error)
        return redirect('cotizador:ver')

    totales = cotizacion.totales(lineas)
    ahora = timezone.localtime()
    comprobante = {'folio': f'COT-{ahora:%Y%m%d-%H%M%S}', 'fecha': ahora}

    cotizacion.vaciar()  # la sesión se vacía al generar el comprobante
    return render(request, 'cotizador/comprobante.html', {
        'comprobante': comprobante,
        'lineas': lineas,
        'totales': totales,
    })