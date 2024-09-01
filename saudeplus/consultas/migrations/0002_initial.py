# Generated by Django 5.0.4 on 2024-08-29 17:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('consultas', '0001_initial'),
        ('medicos', '0001_initial'),
        ('pacientes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='consulta',
            name='medico',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medicos.medico'),
        ),
        migrations.AddField(
            model_name='consulta',
            name='paciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pacientes.paciente'),
        ),
        migrations.AddField(
            model_name='cons_medicamento',
            name='consulta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consultas.consulta'),
        ),
    ]