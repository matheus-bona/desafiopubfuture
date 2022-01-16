from django.db import models
from contas.models import Conta
from django import forms


class TipoDespesa(models.Model):
    tipo_despesa = models.CharField(max_length=100)

    def __str__(self):
        return self.tipo_despesa


class Despesa(models.Model):
    valor = models.DecimalField('Valor da Despesa', decimal_places=2, max_digits=16)
    data_pagamento = models.DateField()
    data_pagamento_esperado = models.DateField()
    tipo_despesa = models.ForeignKey(TipoDespesa, on_delete=models.DO_NOTHING)
    conta_despesa = models.ForeignKey(Conta, on_delete=models.CASCADE, verbose_name='Conta Vinculada')

    def __str__(self):
        return str(self.id)


class FormTipoDespesa(forms.ModelForm):
    class Meta:
        model = TipoDespesa
        exclude = ()


class FormDespesa(forms.ModelForm):
    class Meta:
        model = Despesa
        exclude = ()
        widgets = {
            'data_pagamento': forms.widgets.DateInput(attrs={'type': 'date'}),
            'data_pagamento_esperado': forms.widgets.DateInput(attrs={'type': 'date'})
        }
