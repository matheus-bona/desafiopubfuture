from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('transfer/', views.transfer, name='transfer'),
    path('<int:conta_id>', views.editar_conta, name='editar_conta'),
    path('criar/', views.criar_conta, name='criar_conta'),
    path('criartipo/', views.criar_tipo_conta, name='criar_tipo_conta'),
    path('deletar/', views.deletar_conta, name='deletar_conta'),
]