# Generated by Django 5.0.6 on 2024-05-28 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='button',
            name='description',
            field=models.TextField(blank=True, max_length=10000, null=True, verbose_name='description'),
        ),
    ]
