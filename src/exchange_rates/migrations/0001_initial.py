# Generated by Django 5.1.4 on 2025-01-01 19:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('currencies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExchangeRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.DecimalField(decimal_places=4, max_digits=10)),
                ('base_currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='base_currency', to='currencies.currency')),
                ('target_currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target_currency', to='currencies.currency')),
            ],
            options={
                'indexes': [models.Index(fields=['base_currency', 'target_currency'], name='index_currencies_pair')],
                'constraints': [models.UniqueConstraint(fields=('base_currency', 'target_currency'), name='unique_currencies_pair')],
            },
        ),
    ]
