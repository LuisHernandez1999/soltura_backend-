# Generated by Django 5.1.7 on 2025-05-06 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('averiguacao', '0004_averiguacao_averiguacao_data_20bc65_idx_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='averiguacao',
            name='tipo_servico',
            field=models.CharField(default='Remoção', max_length=50),
        ),
    ]
