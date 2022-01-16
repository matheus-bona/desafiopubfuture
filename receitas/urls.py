from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='receitas'),
    path('cadastrar/', views.cadastrar_receita, name='cadastrar_receita'),
    path('cadastrartipo/', views.cadastrar_tipo_receita, name='cadastrar_tipo_receita'),
    path('<int:receita_id>', views.editar_receita, name='editar_receita'),
    path('deletar=<int:receita_id>', views.deletar_receita, name='deletar_receita'),
    path('filtro', views.filtro_receitas, name='filtro_receitas'),
]

