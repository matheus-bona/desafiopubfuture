from django.db import models
from django import forms


class TipoConta(models.Model):
    tipo_conta = models.CharField(max_length=100, verbose_name='Tipo de Conta')

    def __str__(self):
        return self.tipo_conta


class Conta(models.Model):
    instituicao_financeira = models.CharField('Instituição Financeira', max_length=100)
    saldo = models.DecimalField('Saldo', decimal_places=2, max_digits=16)
    tipo_conta = models.ForeignKey(TipoConta, on_delete=models.DO_NOTHING, verbose_name='Tipo de Conta')

    def __str__(self):
        return str(self.id)


class FormTipoConta(forms.ModelForm):
    class Meta:
        model = TipoConta
        exclude = ()


class FormConta(forms.ModelForm):
    class Meta:
        model = Conta
        exclude = ()

