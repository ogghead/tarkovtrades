# Generated by Django 2.2.11 on 2020-03-13 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20200313_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='trade',
            name='trader_level',
            field=models.CharField(choices=[('I', 1), ('II', 2), ('III', 3), ('Max', 4)], default='I', max_length=200),
            preserve_default=False,
        ),
    ]