# Generated by Django 2.1 on 2020-03-21 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trade',
            name='crafting_station',
            field=models.CharField(blank=True, choices=[('', ''), ('Booze Generator', 'Booze Generator'), ('Intelligence Center', 'Intelligence Center'), ('Lavatory', 'Lavatory'), ('Medstation', 'Medstation'), ('Nutrition Unit', 'Nutrition Unit'), ('Water Collector', 'Water Collector'), ('Workbench', 'Workbench')], default=('', ''), max_length=200),
        ),
        migrations.AddField(
            model_name='trade',
            name='crafting_station_level',
            field=models.CharField(blank=True, choices=[('', ''), ('I', 1), ('II', 2), ('III', 3)], default=('', ''), max_length=200),
        ),
        migrations.AlterField(
            model_name='trade',
            name='trader',
            field=models.CharField(blank=True, choices=[('', ''), ('Prapor', 'Prapor'), ('Therapist', 'Therapist'), ('Fence', 'Fence'), ('Skier', 'Skier'), ('Peacekeeper', 'Peacekeeper'), ('Mechanic', 'Mechanic'), ('Ragman', 'Ragman'), ('Jaeger', 'Jaeger')], default=('', ''), max_length=200),
        ),
        migrations.AlterField(
            model_name='trade',
            name='trader_level',
            field=models.CharField(blank=True, choices=[('', ''), ('I', 1), ('II', 2), ('III', 3), ('Max', 4)], default=('', ''), max_length=200),
        ),
    ]