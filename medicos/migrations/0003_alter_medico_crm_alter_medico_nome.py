# Generated by Django 5.0.4 on 2024-08-31 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicos', '0002_alter_medico_foto_perfil'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medico',
            name='crm',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='medico',
            name='nome',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
