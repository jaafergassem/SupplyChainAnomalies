from django.db import models


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    type=models.IntegerField(null=True)

    distance = models.IntegerField()
    transport_method = models.CharField(max_length=255)
    vendor_CountryCode = models.CharField(max_length=255)
    vendor_poste = models.CharField(max_length=255)
    date_creation = models.DateField()
    date_confirme = models.DateField()
    date_depart = models.DateField()
    unit_cost = models.FloatField()
    unitWeightKG= models.FloatField(default=0.0)
    status_delivery=models.IntegerField(null=True, blank=True)
    livraison_partielle=models.IntegerField(null=True, blank=True)
    date_livraison = models.DateField(null=True, blank=True)
    annomalie_stock = models.CharField(max_length=255,null=True, blank=True)
    etat_stock = models.CharField(max_length=255,null=True, blank=True)

    quantite_commande=models.IntegerField(null=True, blank=True)
    date_livraison_predite= models.DateField(null=True, blank=True)

 


    class Meta:
        db_table = 'core_order'  




from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):

    age = models.PositiveIntegerField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    pass




















# class VendorDimension(models.Model):
#     vendor_CountryCode = models.CharField(max_length=255)
#     vendor_poste = models.CharField(max_length=255)

# class DateDimension(models.Model):
#     date_creation = models.DateField()
#     date_confirme = models.DateField()
#     date_depart = models.DateField()
#     date_livraison = models.DateField(null=True, blank=True)

# class LivraisonDimension(models.Model):
#     transport_method = models.CharField(max_length=255)
#     status_delivery=models.IntegerField(null=True)
#     livraison_partielle=models.IntegerField(null=True)

# class QuantitativesDimension(models.Model):
#     unit_cost = models.FloatField()
#     unitWeightKG= models.FloatField(default=0.0)
#     distance = models.IntegerField()
#     type=models.IntegerField(null=True)


























