# Generated by Django 3.0.3 on 2020-04-09 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_auto_20200408_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tooltype',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='tool_pics/'),
        ),
    ]
