# Generated by Django 3.1.2 on 2020-10-24 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20201024_1854'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='braintree_id',
        ),
        migrations.AddField(
            model_name='order',
            name='braintree_id',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
