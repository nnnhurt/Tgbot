# Generated by Django 5.0.4 on 2024-05-21 17:57

import app.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Button',
            fields=[
                ('created', models.DateTimeField(blank=True, default=app.models.get_datetime, null=True, validators=[app.models.check_date_created], verbose_name='created')),
                ('id', models.SmallAutoField(editable=False, primary_key=True, serialize=False)),
                ('title', models.TextField(max_length=50, verbose_name='title')),
                ('description', models.TextField(blank=True, max_length=500, null=True, verbose_name='description')),
                ('parent_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.button')),
            ],
            options={
                'verbose_name': 'button',
                'verbose_name_plural': 'buttons',
                'db_table': '"django_db"."button"',
                'ordering': ['title', 'description'],
            },
        ),
    ]
