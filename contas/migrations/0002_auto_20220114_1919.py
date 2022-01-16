# Generated by Django 2.2.3 on 2022-01-14 22:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conta',
            name='tipo_conta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='contas.TipoConta', verbose_name='Tipo de Conta'),
        ),
        migrations.AlterField(
            model_name='tipoconta',
            name='tipo_conta',
            field=models.CharField(max_length=100, verbose_name='Tipo de Conta'),
        ),
    ]