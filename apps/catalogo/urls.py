from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    path('', views.lista_productos, name='lista'),
    path('gestion/', views.gestion_productos, name='gestion'),
    path('crear/', views.crear_producto, name='crear'),
    path('<slug:slug>/editar/', views.editar_producto, name='editar'),
    path('<slug:slug>/eliminar/', views.eliminar_producto, name='eliminar'),
    path('<slug:slug>/', views.detalle_producto, name='detalle'),
]