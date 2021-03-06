# Generated by Django 2.1.12 on 2020-03-19 17:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InputCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('true_value', models.IntegerField()),
                ('highest_sell_price_to_trader', models.IntegerField()),
                ('highest_sell_price_trader', models.CharField(choices=[('', ''), ('Prapor', 'Prapor'), ('Therapist', 'Therapist'), ('Fence', 'Fence'), ('Skier', 'Skier'), ('Peacekeeper', 'Peacekeeper'), ('Mechanic', 'Mechanic'), ('Ragman', 'Ragman'), ('Jaeger', 'Jaeger')], max_length=200)),
                ('lowest_buy_price_from_trader', models.IntegerField(blank=True, null=True)),
                ('lowest_buy_price_trader', models.CharField(blank=True, choices=[('', ''), ('Prapor', 'Prapor'), ('Therapist', 'Therapist'), ('Fence', 'Fence'), ('Skier', 'Skier'), ('Peacekeeper', 'Peacekeeper'), ('Mechanic', 'Mechanic'), ('Ragman', 'Ragman'), ('Jaeger', 'Jaeger')], default=('', ''), max_length=200)),
                ('market_buy_price', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='OutputCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=1)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Item')),
            ],
        ),
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trader', models.CharField(choices=[('Prapor', 'Prapor'), ('Therapist', 'Therapist'), ('Fence', 'Fence'), ('Skier', 'Skier'), ('Peacekeeper', 'Peacekeeper'), ('Mechanic', 'Mechanic'), ('Ragman', 'Ragman'), ('Jaeger', 'Jaeger')], max_length=200)),
                ('trader_level', models.CharField(choices=[('I', 1), ('II', 2), ('III', 3), ('Max', 4)], max_length=200)),
                ('input_items', models.ManyToManyField(related_name='inputs', through='app.InputCount', to='app.Item')),
                ('output_items', models.ManyToManyField(related_name='outputs', through='app.OutputCount', to='app.Item')),
            ],
        ),
        migrations.AddField(
            model_name='outputcount',
            name='trade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Trade'),
        ),
        migrations.AddField(
            model_name='inputcount',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Item'),
        ),
        migrations.AddField(
            model_name='inputcount',
            name='trade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Trade'),
        ),
    ]
