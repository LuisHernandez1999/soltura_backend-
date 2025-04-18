# Generated by Django 5.1.7 on 2025-04-12 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soltura', '0004_alter_soltura_tipo_equipe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soltura',
            name='tipo_equipe',
            field=models.CharField(choices=[('Matutino', 'Matutino'), ('Vespertino', 'Vespertino'), ('Noturno', 'Noturno')], default='Equipe1(Matutino)', max_length=20),
        ),
        migrations.AlterField(
            model_name='soltura',
            name='turno',
            field=models.CharField(choices=[('Matutino', 'Matutino'), ('Vespertino', 'Vespertino'), ('Noturno', 'Noturno')], max_length=10),
        ),
    ]
