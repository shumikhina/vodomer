# Generated by Django 3.2.6 on 2021-08-16 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=124)),
            ],
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider_type', models.CharField(choices=[('HW', 'Hot water'), ('CW', 'Cold water'), ('WW', 'Warming water'), ('EL', 'Electricity'), ('GS', 'Gas')], default='CW', max_length=2)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='providers.client')),
            ],
        ),
        migrations.CreateModel(
            name='ProviderValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('received_at', models.DateTimeField(auto_now_add=True)),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='providers.provider')),
            ],
        ),
    ]
