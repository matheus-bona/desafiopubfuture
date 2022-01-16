from django.contrib import admin
from .models import Receita, TipoReceita


class ReceitaAdmin(admin.ModelAdmin):
    list_display = ('id', 'valor', 'data_recebimento', 'data_recebimento_esperado',
                    'tipo_receita',)
    list_display_links = ('id',)
    list_per_page = 25
    search_fields = ('id',)


admin.site.register(Receita, ReceitaAdmin)
admin.site.register(TipoReceita)
