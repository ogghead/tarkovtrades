# Generated by Django 2.2.11 on 2020-03-14 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20200314_1351'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrueValueCalc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('previous_stash', models.IntegerField()),
                ('cashback', models.IntegerField()),
                ('new_stash', models.IntegerField()),
            ],
        ),
    ]