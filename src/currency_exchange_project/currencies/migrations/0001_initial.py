# Generated by Django 5.1.3 on 2024-12-04 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, max_length=3, unique=True)),
                ('full_name', models.CharField(max_length=20)),
                ('sign', models.CharField(max_length=3)),
            ],
        ),
    ]
