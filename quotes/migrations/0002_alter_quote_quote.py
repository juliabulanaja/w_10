# Generated by Django 4.2.4 on 2023-09-21 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='quote',
            field=models.TextField(max_length=300),
        ),
    ]
