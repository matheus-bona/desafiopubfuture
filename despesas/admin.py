from django.contrib import admin
from .models import Despesa, TipoDespesa


class DespesaAdmin(admin.ModelAdmin):
    list_display = ('id', 'valor', 'data_pagamento', 'data_pagamento_esperado',
                    'tipo_despesa',)
    list_display_links = ('id',)
    list_per_page = 25
    search_fields = ('id',)


admin.site.register(Despesa, DespesaAdmin)
admin.site.register(TipoDespesa)
