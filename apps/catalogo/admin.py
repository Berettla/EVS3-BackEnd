from django.contrib import admin
from .models import CategoriaProducto, Producto

# Identidad corporativa del panel
admin.site.site_header = 'Banquetería Judani - Panel de Control'
admin.site.site_title = 'Banquetería Judani Admin'
admin.site.index_title = 'Gestión Operativa de Recursos y Servicios'


@admin.register(CategoriaProducto)
class CategoriaProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activa')
    list_filter = ('activa',)
    search_fields = ('nombre', 'descripcion')


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'categoria', 'precio_unitario', 'estado', 'activo', 'destacado')
    list_filter = ('categoria', 'estado', 'activo', 'destacado')
    search_fields = ('codigo', 'nombre', 'descripcion')
    list_editable = ('precio_unitario', 'estado', 'activo', 'destacado')
    readonly_fields = ('creado',)
    fieldsets = (
        ('Identificación', {
            'fields': ('codigo', 'nombre', 'slug', 'categoria'),
        }),
        ('Detalle del producto', {
            'fields': ('descripcion', 'imagen'),
        }),
        ('Precios y cantidades', {
            'fields': ('precio_unitario', 'pedido_minimo', 'cantidad_maxima'),
        }),
        ('Estado y vigencia', {
            'fields': ('estado', 'activo', 'destacado', 'creado'),
        }),
    )