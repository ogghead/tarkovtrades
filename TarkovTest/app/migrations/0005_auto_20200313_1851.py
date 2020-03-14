# Generated by Django 2.2.11 on 2020-03-14 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_trade_trader_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='highest_sell_price_trader',
            field=models.CharField(choices=[('', ''), ('Prapor', 'Prapor'), ('Therapist', 'Therapist'), ('Fence', 'Fence'), ('Skier', 'Skier'), ('Peacekeeper', 'Peacekeeper'), ('Mechanic', 'Mechanic'), ('Ragman', 'Ragman'), ('Jaeger', 'Jaeger')], max_length=200),
        ),
        migrations.AlterField(
            model_name='item',
            name='lowest_buy_price_from_trader',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='lowest_buy_price_trader',
            field=models.CharField(choices=[('', ''), ('Prapor', 'Prapor'), ('Therapist', 'Therapist'), ('Fence', 'Fence'), ('Skier', 'Skier'), ('Peacekeeper', 'Peacekeeper'), ('Mechanic', 'Mechanic'), ('Ragman', 'Ragman'), ('Jaeger', 'Jaeger')], default=('', ''), max_length=200),
        ),
    ]
