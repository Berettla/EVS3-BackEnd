from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify


class CategoriaProducto(models.Model):
    """Entidad de contexto: agrupa los productos (Empanadas, Canapés, etc.)."""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'categoría'
        verbose_name_plural = 'categorías'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    """Entidad principal: cada producto que se vende o cotiza."""

    class Estado(models.TextChoices):
        DISPONIBLE = 'DISP', 'Disponible'
        AGOTADO = 'AGOT', 'Agotado'
        BAJO_PEDIDO = 'PEDI', 'Bajo pedido'
        TEMPORADA = 'TEMP', 'De temporada'

    categoria = models.ForeignKey(
        CategoriaProducto,
        on_delete=models.PROTECT,
        related_name='productos',
    )
    codigo = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    precio_unitario = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    pedido_minimo = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    cantidad_maxima = models.PositiveIntegerField(default=500, validators=[MinValueValidator(1)])
    estado = models.CharField(max_length=4, choices=Estado.choices, default=Estado.DISPONIBLE)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['categoria__nombre', 'nombre']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.nombre)
            slug = base_slug
            contador = 1
            while Producto.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{contador}"
                contador += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'