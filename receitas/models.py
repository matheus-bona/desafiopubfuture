from django.db import models
from contas.models import Conta
from django import forms


class TipoReceita(models.Model):
    tipo_receita = models.CharField(max_length=100)

    def __str__(self):
        return self.tipo_receita


class Receita(models.Model):
    valor = models.DecimalField('Valor da Receita', decimal_places=2, max_digits=16)
    data_recebimento = models.DateField()
    data_recebimento_esperado = models.DateField()
    tipo_receita = models.ForeignKey(TipoReceita, on_delete=models.DO_NOTHING)
    conta_receita = models.ForeignKey(Conta, on_delete=models.CASCADE, verbose_name='Conta Vinculada')

    def __str__(self):
        return str(self.id)


class FormTipoReceita(forms.ModelForm):
    class Meta:
        model = TipoReceita
        exclude = ()


class FormReceita(forms.ModelForm):
    class Meta:
        model = Receita
        exclude = ()
        widgets = {
            'data_recebimento': forms.widgets.DateInput(attrs={'type': 'date'}),
            'data_recebimento_esperado': forms.widgets.DateInput(attrs={'type': 'date'})
        }
