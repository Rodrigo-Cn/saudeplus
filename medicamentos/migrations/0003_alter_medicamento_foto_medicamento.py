# Generated by Django 5.0.4 on 2024-09-01 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicamentos', '0002_alter_medicamento_nome'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicamento',
            name='foto_medicamento',
            field=models.ImageField(blank=True, max_length=255, upload_to='images/'),
        ),
    ]
