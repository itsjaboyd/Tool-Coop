# Generated by Django 3.0.3 on 2020-03-19 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_auto_20200318_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
