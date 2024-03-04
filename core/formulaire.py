from django.forms import ModelForm
from django import forms 
# from .models import Order, VendorDimension, DateDimension, LivraisonDimension, QuantitativesDimension
from .models import Order
class DateInput(forms.DateInput):
    input_type = 'date'
    format = '%Y-%m-%d'

    
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order 
        # fields = ['distance', 'unit_cost', 'unitWeightKG', 'type', 'date_creation','date_confirme', 'date_depart', 'date_livraison', 'transport_method', 'vendor_CountryCode', 'vendor_poste']
        fields = '__all__'


        widgets = {
                    'date_creation': DateInput(),
                    'date_depart': DateInput(),
                    'date_confirme': DateInput(),
                }





from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('age', 'address', 'phone_number')

        # vendor_dimension = forms.ModelChoiceField(
        #     queryset=VendorDimension.objects.all(),
        #     empty_label=None,  # Pour rendre le champ requis
        # )

        # date_dimension = forms.ModelChoiceField(
        #     queryset=DateDimension.objects.all(),
        #     empty_label=None,
        # )

        # livraison_dimension = forms.ModelChoiceField(
        #     queryset=LivraisonDimension.objects.all(),
        #     empty_label=None,
        # )

        # quantitatives_dimension = forms.ModelChoiceField(
        #     queryset=QuantitativesDimension.objects.all(),
        #     empty_label=None,
        # )










