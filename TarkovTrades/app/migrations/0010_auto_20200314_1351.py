# Generated by Django 2.2.11 on 2020-03-14 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20200313_2133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='fee_to_post_at_buy_price_intel',
        ),
        migrations.RemoveField(
            model_name='item',
            name='fee_to_post_at_buy_price_no_intel',
        ),
        migrations.AddField(
            model_name='item',
            name='true_value',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]