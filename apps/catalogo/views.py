from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductoForm
from .models import CategoriaProducto, Producto

ORDENES = {
    'nombre': 'nombre',
    'precio_asc': 'precio_unitario',
    'precio_desc': '-precio_unitario',
    'recientes': '-creado',
}


def es_personal(user):
    return user.is_staff


# ---------- Catálogo público (Read) ----------

def lista_productos(request):
    productos = Producto.objects.filter(activo=True).select_related('categoria')

    # Búsqueda multi-campo
    q = request.GET.get('q', '').strip()
    if q:
        productos = productos.filter(
            Q(nombre__icontains=q) | Q(codigo__icontains=q) | Q(descripcion__icontains=q)
        )

    # Filtro por categoría
    categoria_id = request.GET.get('categoria', '')
    if categoria_id.isdigit():
        productos = productos.filter(categoria_id=categoria_id)

    # Ordenamiento
    orden = request.GET.get('orden', 'nombre')
    productos = productos.order_by(ORDENES.get(orden, 'nombre'))

    # Paginación
    paginator = Paginator(productos, 6)
    pagina = paginator.get_page(request.GET.get('page'))

    return render(request, 'catalogo/lista.html', {
        'pagina': pagina,
        'categorias': CategoriaProducto.objects.filter(activa=True),
        'q': q,
        'categoria_id': categoria_id,
        'orden': orden,
    })


def detalle_producto(request, slug):
    producto = get_object_or_404(
        Producto.objects.select_related('categoria'), slug=slug, activo=True
    )
    return render(request, 'catalogo/detalle.html', {'producto': producto})


# ---------- Backoffice (solo personal) ----------

@login_required
@user_passes_test(es_personal, login_url='core:acceso_denegado')
def gestion_productos(request):
    productos = Producto.objects.select_related('categoria').order_by('categoria__nombre', 'nombre')
    return render(request, 'catalogo/gestion.html', {'productos': productos})


@login_required
@user_passes_test(es_personal, login_url='core:acceso_denegado')
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto.nombre}" creado correctamente.')
            return redirect('catalogo:detalle', slug=producto.slug)
    else:
        form = ProductoForm()
    return render(request, 'catalogo/form.html', {'form': form, 'titulo': 'Nuevo producto'})


@login_required
@user_passes_test(es_personal, login_url='core:acceso_denegado')
def editar_producto(request, slug):
    producto = get_object_or_404(Producto, slug=slug)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto.nombre}" actualizado correctamente.')
            return redirect('catalogo:gestion')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'catalogo/form.html', {
        'form': form,
        'titulo': f'Editar: {producto.nombre}',
    })


@login_required
@user_passes_test(es_personal, login_url='core:acceso_denegado')
def eliminar_producto(request, slug):
    producto = get_object_or_404(Producto, slug=slug, activo=True)
    if request.method == 'POST':
        producto.activo = False
        producto.save(update_fields=['activo'])
        messages.success(
            request,
            f'El producto "{producto.nombre}" fue desactivado y ya no aparece en el catálogo.',
        )
        return redirect('catalogo:gestion')
    return render(request, 'catalogo/confirmar_eliminar.html', {'producto': producto})