# Generated by Django 4.2.3 on 2023-10-12 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='annomalie_stock',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='date_livraison_predite',
            field=models.DateField(blank=True, null=True),
        ),
    ]
