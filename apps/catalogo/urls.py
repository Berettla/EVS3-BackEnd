from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    path('', views.lista_productos, name='lista'),
    path('crear/', views.crear_producto, name='crear'),
    path('<slug:slug>/', views.detalle_producto, name='detalle'),
]