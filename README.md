# Banquetería Judani

Aplicación web desarrollada con Django para una banquetería: catálogo público de productos, cotizador guardado en sesión y panel de gestión protegido por roles.

## Ficha de registro

| Campo | Detalle |
|---|---|
| **Nombre de la Organización o Plataforma** | Banquetería Judani |
| **Modelo de Negocio / Giro** | Banquetería y catering para eventos |
| **Integrantes del Equipo** | Agustín Narciso Inzunza Montecinos - 21.897.856-8 |
| **Entidad de Contexto / Agrupación (ORM)** | `CategoriaProducto` |
| **Entidad Principal Gestionable (ORM)** | `Producto` |
| **Propósito de la Sesión (request.session)** | Cotizador de productos para eventos: selección de productos con cantidades (validando pedido mínimo, máximo por cotización y disponibilidad) y cálculo de subtotal, IVA (19%) y total, con comprobante simulado |

## Funcionalidades

**1. Catálogo público**
- Tarjetas de productos con imagen, categoría, estado, precio y pedido mínimo.
- Búsqueda multi-campo (nombre, código y descripción) con objetos `Q`.
- Filtro por categoría, ordenamiento (nombre, precio, más recientes) y paginación con `Paginator`.
- Ficha de detalle por `slug`, y botón para limpiar los filtros.
- Inicio con carrusel, productos destacados y sección "¿Cómo funciona?".

**2. Cotizador en sesión (`request.session`)**
- Agregar productos validando disponibilidad, pedido mínimo y cantidad máxima por cotización.
- Modificar cantidades, quitar un producto o vaciar la cotización.
- Desglose de subtotal, IVA (19%) y total. Los precios del catálogo son netos.
- Context Processor que muestra el contador de productos en el navbar.
- Solicitud de cotización (requiere sesión iniciada): genera un comprobante simulado y vacía la sesión.

**3. Backoffice protegido**
- CRUD completo en el sitio (panel de gestión) para el personal (`is_staff`).
- Eliminación como baja lógica con pantalla de confirmación; el producto se puede reactivar editándolo.
- Django Admin personalizado con título corporativo, `list_display`, `list_filter`, `search_fields`, `list_editable` y `fieldsets`.

**Autenticación y roles**
- Registro, login y logout con `django.contrib.auth`.
- Perfil de usuario (RUT, teléfono y rol), con validación de RUT y correo únicos y teléfono normalizado a formato `+569XXXXXXXX`.
- Rutas administrativas protegidas con `@login_required` y `@user_passes_test(is_staff)`; quien no es personal ve una página de acceso denegado.
- Protección CSRF (`{% csrf_token %}`) en todos los formularios POST.

## Tecnologías

- Python 3.12 o superior y Django 6.1 (versión fijada en `requirements.txt`)
- Pillow (manejo de imágenes) y python-dotenv (variables de entorno)
- Bootstrap 5 y Bootstrap Icons (por CDN)
- SQLite (base de datos por defecto de Django)

## Estructura del proyecto

```
├── config/            Configuración del proyecto (settings, urls)
├── apps/
│   ├── catalogo/      Modelos, admin, CRUD y catálogo público
│   ├── cotizador/     Cotización en sesión y context processor
│   ├── usuarios/      Registro, login, logout y perfil
│   └── core/          Inicio y página de acceso denegado
├── templates/         Plantillas (base.html y una carpeta por app)
├── static/            Imágenes del sitio (portadas del carrusel)
├── media/             Imágenes de productos subidas (no se versiona)
├── .env.example       Ejemplo de variables de entorno
└── requirements.txt   Dependencias con versiones fijas
```

## Instalación paso a paso

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/Berettla/EVS3-BackEnd.git
   cd EVS3-BackEnd
   ```

2. **Crear y activar el entorno virtual**
   ```bash
   python -m venv .venv
   ```
   - Windows: `.venv\Scripts\activate`
   - Mac/Linux: `source .venv/bin/activate`

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Crear el archivo `.env`** a partir del ejemplo `.env.example` del repositorio
   - Windows: `copy .env.example .env`
   - Mac/Linux: `cp .env.example .env`

   Luego genera una clave secreta y pégala como valor de `SECRET_KEY` en el `.env`:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(50))"
   ```

5. **Aplicar migraciones**
   ```bash
   python manage.py migrate
   ```

6. **Cargar datos de prueba** (5 categorías, 10 productos, usuarios y perfiles)
   ```bash
   python manage.py poblar_datos
   ```

7. **Iniciar el servidor**
   ```bash
   python manage.py runserver
   ```
   Abre `http://127.0.0.1:8000/`.

## Credenciales de prueba

| Rol | Usuario | Contraseña | Acceso |
|---|---|---|---|
| Administrador | `admin` | `admin12345` | Todo el sitio, panel de gestión y `/admin/` |
| Cliente | `cliente` | `cliente12345` | Catálogo y cotizador |

Cualquier persona puede además registrarse desde `/usuarios/registro/` (queda con rol Cliente).

## Rutas principales

| Ruta | Descripción | Acceso |
|---|---|---|
| `/` | Inicio | Público |
| `/catalogo/` | Catálogo con búsqueda, filtros y paginación | Público |
| `/catalogo/<slug>/` | Detalle de un producto | Público |
| `/cotizador/` | Mi cotización | Público |
| `/cotizador/confirmar/` | Solicitar cotización y ver comprobante | Sesión iniciada |
| `/usuarios/registro/`, `/usuarios/login/` | Registro e inicio de sesión | Público |
| `/catalogo/gestion/` | Panel de gestión de productos | Personal |
| `/catalogo/crear/` | Crear producto | Personal |
| `/catalogo/<slug>/editar/` | Editar producto | Personal |
| `/catalogo/<slug>/eliminar/` | Desactivar producto (con confirmación) | Personal |
| `/admin/` | Django Admin personalizado | Personal |

## Decisiones de diseño

- **Baja lógica:** los productos se desactivan (`activo = False`) en vez de borrarse; las categorías con productos no se pueden eliminar (`on_delete=PROTECT`).
- **Cotización en sesión:** solo se guardan identificadores y cantidades; los precios se leen de la base de datos en cada vista, para que nunca queden desactualizados. La disponibilidad se revalida al solicitar la cotización.
- **Roles:** el rol de un usuario nuevo siempre es Cliente y se define en el servidor, nunca desde el formulario.
- **Variables sensibles** (`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`) en `.env`, que no se versiona.

## Bitácora de prompts (uso de IA)

Usé Claude (Anthropic) como apoyo en arquitectura, ORM y seguridad. En todos los casos revisé, probé y adapté el código antes de integrarlo.

### Caso 1: Arquitectura y modelado (ORM)

**Prompt:** "Mi proyecto es una banquetería con catálogo de productos (empanadas, canapés, etc.) y cotizaciones para eventos. Según la rúbrica necesito una entidad de contexto y una principal con ForeignKey PROTECT, MinValueValidator, choices, ImageField y baja lógica. ¿Cómo los modelo?"

**Respuesta técnica (resumen):** Propuso `CategoriaProducto` y `Producto`, con `ForeignKey(on_delete=PROTECT, related_name='productos')`, `TextChoices` para el estado, `MinValueValidator` en precio y cantidades, `ImageField`, un campo `activo` para la baja lógica y un `slug` único generado en `save()`. Sugirió además `pedido_minimo` y `cantidad_maxima`.

**Adaptación aplicada:**
- Conservé `pedido_minimo` y `cantidad_maxima` porque en banquetería se vende por unidades mínimas y la cantidad máxima me sirve como control de cupos en el cotizador.
- La IA generaba el slug con `slugify(codigo + nombre)`. Lo reemplacé por la versión vista en clases, con un bucle que usa `.exists()`, porque no depende de que el código esté bien escrito y deja URLs más limpias. Al integrarla cometí un error de sangría que provocaba `UnboundLocalError` al editar un producto; lo corregí entendiendo que el cálculo del slug debe ir completo dentro del `if not self.slug`.
- Agregué el campo `destacado` para elegir qué productos aparecen en el inicio.
- Decidí mantener el código del producto ingresado por el personal, en lugar de generarlo automáticamente, porque muchos negocios ya manejan sus propios códigos.

### Caso 2: Consultas con el ORM

**Prompt:** "¿Cómo hago un catálogo con búsqueda en varios campos, filtro por categoría, ordenamiento y paginación, sin hacer consultas innecesarias?"

**Respuesta técnica (resumen):** Usar objetos `Q` con `icontains` para buscar en nombre, código y descripción a la vez; `select_related('categoria')` para evitar una consulta extra por cada tarjeta; y `Paginator.get_page()` para paginar.

**Adaptación aplicada:**
- El orden lo resolví con un diccionario fijo (`ORDENES`) en lugar de pasar el parámetro de la URL directamente a `order_by()`, para que el usuario no pueda ordenar por campos arbitrarios. También valido el filtro de categoría con `isdigit()`.
- Al probar noté que se perdía la búsqueda y la página al entrar a un detalle y volver, así que conservé los filtros reutilizando `request.GET.urlencode` en los enlaces.
- Agregué un botón "Limpiar" que aparece solo cuando hay filtros activos.

### Caso 3: Seguridad y control de acceso

**Prompt:** "¿Cómo protejo las vistas del CRUD para que solo el personal pueda crear, editar y eliminar, y cómo evito que alguien se registre como administrador?"

**Respuesta técnica (resumen):** Combinar `@login_required` con `@user_passes_test(is_staff)`; incluir `{% csrf_token %}` en todos los formularios POST; fijar el rol en el servidor (en el `save()` del formulario) y no leerlo del formulario; usar POST para el logout.

**Adaptación aplicada:**
- `user_passes_test` manda al login incluso a un cliente que ya inició sesión, lo que confundía. Lo resolví con `login_url='core:acceso_denegado'` y una página 403 propia: el visitante sin sesión va al login y el cliente ve "Acceso denegado".
- El enlace "Gestión" y el acceso al panel de administración solo se muestran a usuarios del personal.
- Agregué validaciones que no venían en el ejemplo base: correo único, RUT con formato y único, y teléfono normalizado al formato `+569XXXXXXXX`.

### Caso 4: Colección en sesión (cotizador)

**Prompt:** "¿Cómo implemento una colección en `request.session` con validación de cupos, cálculo de IVA y un contador global en el navbar?"

**Respuesta técnica (resumen):** Encapsular la lógica en una clase que envuelve la sesión, guardar una estructura `{id_producto: cantidad}`, marcar `session.modified = True` al cambiarla y exponer el contador mediante un Context Processor.

**Adaptación aplicada:**
- Guardo solo ids y cantidades, no precios: los precios se leen de la base de datos, así que no quedan desactualizados si el personal los cambia.
- Al solicitar la cotización vuelvo a validar la disponibilidad, porque un producto puede agotarse mientras está en la cotización.
- El IVA se calcula con enteros y redondeo al peso, porque el peso chileno no usa decimales. Los precios del catálogo se consideran netos.
- La solicitud exige iniciar sesión, para asociar el comprobante a un cliente; armar la cotización es libre.