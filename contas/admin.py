from django.contrib import admin
from .models import Conta, TipoConta


class ContaAdmin(admin.ModelAdmin):
    list_display = ('id', 'instituicao_financeira', 'tipo_conta')
    list_display_links = ('id',)
    list_per_page = 25
    search_fields = ('id',)


admin.site.register(Conta, ContaAdmin)
admin.site.register(TipoConta)
