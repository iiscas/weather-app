# Generated by Django 4.2.17 on 2024-12-16 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('umbrella', '0002_weatherforecast_delete_forecast'),
    ]

    operations = [
        migrations.CreateModel(
            name='Forecast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100)),
                ('temperature', models.FloatField()),
                ('description', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='WeatherForecast',
        ),
    ]
