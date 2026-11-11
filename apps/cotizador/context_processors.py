def cotizacion_contador(request):
    """Inyecta en todas las plantillas la cantidad de productos en la cotización."""
    return {'cotizacion_items': len(request.session.get('cotizacion', {}))}