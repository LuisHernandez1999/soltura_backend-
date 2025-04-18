# Generated by Django 5.1.7 on 2025-04-01 19:47

import apps.veiculos.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Veiculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prefixo', models.CharField(max_length=10, unique=True)),
                ('tipo', models.CharField(choices=[('Basculante', 'Basculante'), ('Selectolix', 'Selectolix'), ('Baú', 'Baú')], max_length=20)),
                ('placa_veiculo', models.CharField(max_length=8, unique=True, validators=[apps.veiculos.models.VeiculoValidator.validar_placa])),
                ('status', models.CharField(choices=[('Ativo', 'Ativo'), ('Inativo', 'Inativo')], default='Ativo', max_length=10, verbose_name='Status do Veículo')),
                ('motivo_inatividade', models.CharField(blank=True, choices=[('Em Manutenção', 'Em Manutenção'), ('Em Garagem', 'Em Garagem')], max_length=20, null=True, verbose_name='Motivo da Inatividade')),
                ('data_manutencao', models.DateTimeField(blank=True, null=True, verbose_name='Data de Início da Manutenção')),
                ('data_saida', models.DateTimeField(blank=True, null=True, verbose_name='Data de Saída da Manutenção')),
                ('custo_manutencao', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Custo da Manutenção')),
            ],
            options={
                'db_table': 'veiculo',
            },
        ),
        migrations.CreateModel(
            name='HistoricoManutencao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_manutencao', models.DateTimeField(verbose_name='Data de Início da Manutenção')),
                ('data_saida', models.DateTimeField(verbose_name='Data de Saída da Manutenção')),
                ('custo_manutencao', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Custo da Manutenção')),
                ('descricao_manutencao', models.TextField(verbose_name='Descrição da Manutenção')),
                ('veiculo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manutencao_historico', to='veiculos.veiculo')),
            ],
            options={
                'db_table': 'historico_manutencao',
            },
        ),
    ]
