from django.urls import path
from . import views

app_name = 'cotizador'

urlpatterns = [
    path('', views.ver_cotizacion, name='ver'),
    path('agregar/<int:producto_id>/', views.agregar, name='agregar'),
    path('actualizar/<int:producto_id>/', views.actualizar, name='actualizar'),
    path('quitar/<int:producto_id>/', views.quitar, name='quitar'),
    path('vaciar/', views.vaciar, name='vaciar'),
    path('confirmar/', views.confirmar, name='confirmar'),
]