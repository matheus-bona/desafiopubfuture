# Generated by Django 2.2.3 on 2022-01-16 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receitas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receita',
            name='valor',
            field=models.DecimalField(decimal_places=2, max_digits=16, verbose_name='Valor da Receita'),
        ),
    ]