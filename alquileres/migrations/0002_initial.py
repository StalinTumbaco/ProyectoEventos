# Generated by Django 5.1.4 on 2024-12-10 02:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('alquileres', '0001_initial'),
        ('eventos', '0001_initial'),
        ('servicios', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='alquiler',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='alquiler',
            name='evento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventos.evento'),
        ),
        migrations.AddField(
            model_name='alquilerservicio',
            name='alquiler',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alquileres.alquiler'),
        ),
        migrations.AddField(
            model_name='alquilerservicio',
            name='servicio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='servicios.servicio'),
        ),
        migrations.AddField(
            model_name='fotoalquiler',
            name='evento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventos.evento'),
        ),
    ]
