from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='despesas'),
    path('cadastrar/', views.cadastrar_despesa, name='cadastrar_despesa'),
    path('cadastrartipo/', views.cadastrar_tipo_despesa, name='cadastrar_tipo_despesa'),
    path('<int:despesa_id>', views.editar_despesa, name='editar_despesa'),
    path('deletar=<int:despesa_id>', views.deletar_despesa, name='deletar_despesa'),
    path('filtro', views.filtro_despesas, name='filtro_despesas'),
]
