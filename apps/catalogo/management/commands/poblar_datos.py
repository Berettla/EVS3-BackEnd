from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.catalogo.models import CategoriaProducto, Producto


class Command(BaseCommand):
    help = "Pobla la base de datos con categorías, productos y usuarios de prueba."

    def handle(self, *args, **kwargs):
        # Usuarios de prueba
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@banqueteria.cl", "admin12345")
            self.stdout.write(self.style.SUCCESS("✓ Superusuario 'admin' creado."))

        if not User.objects.filter(username="cliente").exists():
            User.objects.create_user("cliente", "cliente@banqueteria.cl", "cliente12345")
            self.stdout.write(self.style.SUCCESS("✓ Usuario 'cliente' creado."))

        # Categorías
        categorias = {
            "Empanadas": "Empanadas horneadas y fritas para cócteles y eventos.",
            "Canapés": "Bocadillos fríos y calientes para recepciones.",
            "Platos de fondo": "Platos principales por porción para banquetes.",
            "Postres": "Dulces individuales y tartaletas.",
            "Bebidas": "Jugos, limonadas y bebidas para eventos.",
        }
        cat_map = {}
        for nombre, desc in categorias.items():
            cat, _ = CategoriaProducto.objects.get_or_create(
                nombre=nombre, defaults={"descripcion": desc}
            )
            cat_map[nombre] = cat

        # Productos: (codigo, nombre, categoria, precio, pedido_minimo, cantidad_maxima, estado, descripcion)
        productos = [
            ("EMP-001", "Empanada de pino", cat_map["Empanadas"], 1800, 12, 500, "DISP", "Clásica empanada de pino horneada."),
            ("EMP-002", "Empanada de queso", cat_map["Empanadas"], 1600, 12, 500, "DISP", "Empanada frita rellena de queso."),
            ("CAN-001", "Canapé de salmón", cat_map["Canapés"], 1500, 20, 300, "DISP", "Pan crocante con queso crema y salmón."),
            ("CAN-002", "Canapé de jamón y queso", cat_map["Canapés"], 900, 20, 400, "DISP", "Bocadillo clásico de jamón y queso."),
            ("PLA-001", "Pollo al jugo con arroz", cat_map["Platos de fondo"], 6500, 10, 200, "PEDI", "Porción individual con acompañamiento."),
            ("PLA-002", "Lomo saltado", cat_map["Platos de fondo"], 8000, 10, 150, "PEDI", "Lomo salteado con papas fritas y arroz."),
            ("POS-001", "Tartaleta de frutilla", cat_map["Postres"], 1200, 12, 300, "DISP", "Tartaleta con crema pastelera y frutilla."),
            ("POS-002", "Mini cheesecake", cat_map["Postres"], 1400, 12, 250, "TEMP", "Cheesecake individual con salsa de frutos rojos."),
            ("BEB-001", "Jugo natural", cat_map["Bebidas"], 1000, 20, 400, "DISP", "Vaso de jugo natural de temporada."),
            ("BEB-002", "Limonada de menta", cat_map["Bebidas"], 900, 20, 400, "AGOT", "Limonada fresca con menta y jengibre."),
        ]
        for cod, nom, cat, pre, minimo, maximo, est, desc in productos:
            Producto.objects.get_or_create(
                codigo=cod,
                defaults={
                    "nombre": nom,
                    "categoria": cat,
                    "precio_unitario": pre,
                    "pedido_minimo": minimo,
                    "cantidad_maxima": maximo,
                    "estado": est,
                    "descripcion": desc,
                    "activo": True,
                },
            )

        self.stdout.write(self.style.SUCCESS("✓ Catálogo poblado exitosamente."))