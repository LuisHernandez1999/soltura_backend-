# Generated by Django 5.1.7 on 2025-04-16 13:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soltura', '0010_alter_soltura_rota'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soltura',
            name='hora_chegada',
            field=models.TimeField(default=datetime.time(14, 14), null=True),
        ),
    ]
