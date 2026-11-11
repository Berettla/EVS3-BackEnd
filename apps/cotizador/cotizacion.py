from apps.catalogo.models import Producto

IVA_PORCENTAJE = 19


class CotizacionError(Exception):
    """Error de validación de la cotización (se muestra al usuario)."""


class Cotizacion:
    """cotización guardada en request.session (sin guardar en la base de datos).

    Estructura en sesión: {'<id_producto>': cantidad}
    """
    SESSION_KEY = 'cotizacion'

    def __init__(self, request):
        self.session = request.session
        self.items = self.session.get(self.SESSION_KEY, {})

    def __len__(self):
        return len(self.items)

    def _guardar(self):
        self.session[self.SESSION_KEY] = self.items
        self.session.modified = True

    def _validar_cantidad(self, producto, cantidad):
        if not producto.activo or producto.estado == Producto.Estado.AGOTADO:
            raise CotizacionError(f'"{producto.nombre}" no está disponible por el momento.')
        if cantidad < producto.pedido_minimo:
            raise CotizacionError(
                f'El pedido mínimo de "{producto.nombre}" es de {producto.pedido_minimo} unidades.'
            )
        if cantidad > producto.cantidad_maxima:
            raise CotizacionError(
                f'El máximo por cotización de "{producto.nombre}" es de {producto.cantidad_maxima} unidades.'
            )

    def agregar(self, producto, cantidad):
        total = self.items.get(str(producto.id), 0) + cantidad
        self._validar_cantidad(producto, total)
        self.items[str(producto.id)] = total
        self._guardar()

    def actualizar(self, producto, cantidad):
        if str(producto.id) not in self.items:
            raise CotizacionError('Ese producto no está en tu cotización.')
        self._validar_cantidad(producto, cantidad)
        self.items[str(producto.id)] = cantidad
        self._guardar()

    def quitar(self, producto_id):
        self.items.pop(str(producto_id), None)
        self._guardar()

    def vaciar(self):
        self.items = {}
        self._guardar()

    def lineas(self):
        productos = (
            Producto.objects
            .filter(id__in=[int(i) for i in self.items])
            .select_related('categoria')
            .order_by('categoria__nombre', 'nombre')
        )
        return [
            {
                'producto': p,
                'cantidad': self.items[str(p.id)],
                'subtotal': p.precio_unitario * self.items[str(p.id)],
            }
            for p in productos
        ]

    def totales(self, lineas):
        subtotal = sum(linea['subtotal'] for linea in lineas)
        iva = (subtotal * IVA_PORCENTAJE + 50) // 100
        return {'subtotal': subtotal, 'iva': iva, 'total': subtotal + iva}

    def errores_disponibilidad(self, lineas):
        """Revisa de nuevo cada línea (el producto pudo cambiar de estado)."""
        errores = []
        for linea in lineas:
            try:
                self._validar_cantidad(linea['producto'], linea['cantidad'])
            except CotizacionError as error:
                errores.append(str(error))
        return errores