from django import forms

from .models import Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'codigo', 'nombre', 'categoria', 'estado', 'descripcion',
            'precio_unitario', 'pedido_minimo', 'cantidad_maxima', 'imagen', 'activo','destacado',
        ]
        labels = {
            'codigo': 'Código',
            'categoria': 'Categoría',
            'descripcion': 'Descripción',
            'precio_unitario': 'Precio unitario (CLP)',
            'pedido_minimo': 'Pedido mínimo (unidades)',
            'cantidad_maxima': 'Cantidad máxima por cotización',
            'imagen': 'Imagen',
            'activo': 'Visible en el catálogo',
            'destacado': 'Mostrar como destacado en el inicio',
        }
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: EMP-003'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'pedido_minimo': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'cantidad_maxima': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'destacado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_codigo(self):
        codigo = self.cleaned_data['codigo'].strip().upper()
        existe = Producto.objects.filter(codigo__iexact=codigo).exclude(pk=self.instance.pk)
        if existe.exists():
            raise forms.ValidationError('Ya existe un producto con este código.')
        return codigo

    def clean_precio_unitario(self):
        precio = self.cleaned_data['precio_unitario']
        if precio < 0:
            raise forms.ValidationError('El precio no puede ser negativo.')
        return precio

    def clean(self):
        datos = super().clean()
        minimo = datos.get('pedido_minimo')
        maximo = datos.get('cantidad_maxima')
        if minimo and maximo and minimo > maximo:
            self.add_error('pedido_minimo', 'El pedido mínimo no puede superar la cantidad máxima.')
        return datos