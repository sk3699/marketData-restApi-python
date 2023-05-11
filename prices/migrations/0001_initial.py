# Generated by Django 4.1.3 on 2023-05-10 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MarketData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('option', models.CharField(max_length=3)),
                ('delivery_month', models.CharField(max_length=5)),
                ('PV', models.CharField(max_length=50)),
                ('call_put', models.CharField(max_length=4)),
                ('price', models.FloatField()),
                ('currency_units', models.CharField(max_length=10)),
            ],
        ),
    ]
