# Generated by Django 4.2.3 on 2023-10-20 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_order_etat_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='quantite_commande',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
