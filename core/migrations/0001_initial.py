# Generated by Django 3.2.3 on 2022-04-18 14:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider_type', models.CharField(choices=[('HW', 'Hot water'), ('CW', 'Cold water'), ('WW', 'Warming water'), ('EL', 'Electricity'), ('GS', 'Gas')], default='CW', max_length=2)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.client')),
            ],
        ),
        migrations.CreateModel(
            name='ProviderValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('created_at', models.DateTimeField()),
                ('received_at', models.DateTimeField(auto_now_add=True)),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.provider')),
            ],
        ),
    ]
