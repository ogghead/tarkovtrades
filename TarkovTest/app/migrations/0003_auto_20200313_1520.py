# Generated by Django 2.2.11 on 2020-03-13 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20200313_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inputcount',
            name='amount',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='outputcount',
            name='amount',
            field=models.IntegerField(default=1),
        ),
    ]
