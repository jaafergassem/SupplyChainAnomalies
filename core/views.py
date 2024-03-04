from django.contrib.auth.models import User, Group

from rest_framework import generics,permissions,viewsets
from .models import Order, CustomUser
from django.views import View
from .serializers import CustomUserSerializer, GroupSerializer, OrderSerializer
from datetime import datetime


from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils.decorators import method_decorator
from .apps import CoreConfig
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse

from django.shortcuts import render, redirect
from .models import Order

from django.shortcuts import render, redirect
from .formulaire import OrderForm

from django.views.decorators.cache import never_cache

@never_cache
def ajouter_commande(request):
    if not request.user.is_authenticated:
        return redirect('core:sing_in')
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            commande = form.instance
            return redirect('core:list_commandes') 

        
     
          
    else:
        form = OrderForm()
    
    return render(request, 'orderform.html', {'form': form})


@never_cache
def lister_commandes(request):
    if not request.user.is_authenticated:
       return redirect('core:sing_in')
    
    commandes = Order.objects.all()
    return render(request, 'result.html', {'commandes': commandes})



from django.shortcuts import render, get_object_or_404, redirect
@never_cache
def modifier_commande(request, id):
    if not request.user.is_authenticated:
        return redirect('core:sing_in')
    
    commande = get_object_or_404(Order, id=id)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=commande)
        if form.is_valid():
            form.save()
            return redirect('core:list_commandes') 
    else:
        form = OrderForm(instance=commande)

    return render(request, 'modifier_commande.html', {'form': form, 'commande': commande})










from django.shortcuts import render, get_object_or_404, redirect
from core.models import Order  
@never_cache
def supprimer_commande(request, id):

    if not request.user.is_authenticated:
        return redirect('core:sing_in')
    
    if request.method == 'POST':
        try:
            commande = Order.objects.get(id=id)
            commande.delete()
        except Order.DoesNotExist:
            return redirect('core:list_commandes')
        return redirect('core:list_commandes') 
    else:
        try:
            commande = Order.objects.get(id=id)
        except Order.DoesNotExist:
            return redirect('core:list_commandes')
    return render(request, 'supprimer_commande.html', {'commande': commande})




def formulaire(request):
    return render(request, 'formulaire.html')

def resultat(request):
    return render(request, 'resultat.html')

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer




def get_commandes_data(request):
    commandes = Order.objects.all().values('id', 'distance')
    data = list(commandes)
    return JsonResponse(data, safe=False)






from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages



from .formulaire import CustomUserCreationForm
def sing_up(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:sing_in')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})







def sing_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('core:dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')


def log_out(request):
    logout(request)
    return redirect('core:sing_in') 




from django.views.decorators.cache import never_cache

@never_cache
def dashboard(request):


    if not request.user.is_authenticated:
        return redirect('core:sing_in')
    
    orders = Order.objects.all()


    rupture_stock_count = orders.filter(etat_stock='rupture').count()

    en_stock_count = orders.filter(etat_stock='en_stock').count()

    initial_data = {
        'Advance_time_delivry': orders.filter(status_delivery=0).count(),
        'On_time_delivry':  orders.filter(status_delivery=2).count(),
        'Late_time_delivry': orders.filter(status_delivery=1).count(),
         'rupture': rupture_stock_count,
        'en_stock': en_stock_count,
    }

    return render(request, 'dashboard.html', {'initial_data': initial_data})











class CustomUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows CustomUsers to be viewed or edited.
    """
    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]




@method_decorator(never_cache, name='dispatch')
class TableauxPredictionView(View):
  

    
    template_name = 'tableaux_prediction.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('core:sing_in')
        commandes = Order.objects.all()
        return render(request, self.template_name, {'commandes': commandes})

    def post(self, request):
        selected_commandes = request.POST.getlist('commande_id')

        

        for id in selected_commandes:
            commande = Order.objects.get(id=id)
 

            if commande.transport_method == "avion":
                transport_method_encoded = 0
            elif commande.transport_method == "bateau":
                transport_method_encoded = 1
            elif commande.transport_method == "camion":
                transport_method_encoded = 2
            else:
                transport_method_encoded = -1



            type = commande.type
            distance = commande.distance
            date_creation = commande.date_creation
            date_depart = commande.date_depart
            date_confirme = commande.date_confirme

         
            unit_cost = commande.unit_cost
            unitWeightKG = commande.unitWeightKG
            vendor_CountryCode = commande.vendor_CountryCode
            vendor_poste = commande.vendor_poste

            data = {
                'distance': distance,
                'Transport Method': float(transport_method_encoded),
                'Days for shipment (scheduled)': (date_confirme - date_creation).days,
                'les jours de depart de fournisseur': (date_depart - date_creation).days,
                'Unit Cost (LCY)': unit_cost,
                'Vendor_CountryCode': vendor_CountryCode,
                'vendor_poste': vendor_poste,
                # 'status_delivery': commande.status_delivery,
                # 'Livraison partielle': commande.livraison_partielle,
                'status_delivery': 1,
                'Livraison partielle': 1,
                'UnitWeightKG': unitWeightKG
            }

            df = pd.DataFrame(data, index=[0])



            from sklearn.preprocessing import LabelEncoder

            # Créer une instance de LabelEncoder
            label_encoder = LabelEncoder()
            df['Vendor_CountryCode'] = label_encoder.fit_transform(df['Vendor_CountryCode'])
            df['vendor_poste'] = label_encoder.fit_transform(df['vendor_poste'])


            model = CoreConfig.model
            result = model.predict(df)

            result = int(result)

            # Ajouter les jours prédits à la date de création de la commande
            date_livraison = pd.Timestamp(date_creation) + pd.DateOffset(days=result)
            date_livraison=date_livraison.date()

            date_livraison_predite=date_livraison.isoformat()

            commande.date_livraison_predite = date_livraison_predite
            commande.save()

        return redirect('core:tableaux-prediction')








     
# @method_decorator(csrf_exempt, name='dispatch')
@method_decorator(never_cache, name='dispatch')

class TableauxPredictionAnnomalieView(View):
  
    template_name = 'tableaux_prediction_annomalie.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('core:sing_in')
        commandes = Order.objects.all()
        return render(request, self.template_name, {'commandes': commandes})
    

    def post(self, request):

      
        selected_commandes = request.POST.getlist('commande_id')
        for id in selected_commandes:
            commande = Order.objects.get(id=id)
 
            type_commande = commande.type
            date_creation = commande.date_creation
            unit_cost = commande.unit_cost
         
    
            month = date_creation.month
            data = json.dumps({
                'Type': type_commande,
                'Unit Cost (LCY)': unit_cost,
                'month':month,
                
            })

  
            df = pd.json_normalize(data={
                'Type': type_commande,
                'Unit Cost (LCY)': unit_cost,
                'month':month,
            })
     
      
            model = CoreConfig.model2 
            result = model.predict(df)
            print(result)

            if commande.annomalie_stock == 1:
                            month = "Octobre"  # Remplacez par le mois concerné.
                            script = f"showStockShortageNotification({commande.id}, '{month}');"

                            # Incluez le script dans le contexte pour le rendre accessible dans le modèle.
                            context = {'notification_script': script}

                            return render(request, self.template_name, context)


 


            result = int(result)
            commande.annomalie_stock = result

            commande.save()

        return redirect('core:tableaux-prediction-annomalie')





@method_decorator(never_cache, name='dispatch')

class DeliveryDatePredictionViewSet(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('core:sing_in')
        form = OrderForm()
        return render(request, 'formulaire.html', {'form': form})
    def post(self, request):

        form = OrderForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            type = data['type']
            distance = data['distance']
            transport_method = data['transport_method']
            date_creation = pd.to_datetime(data['date_creation'], format='%d/%m/%Y')
            date_depart = pd.to_datetime(data['date_depart'], format='%d/%m/%Y')
            date_confirme = pd.to_datetime(data['date_confirme'], format='%d/%m/%Y')
            unit_cost = data['unit_cost']
            # status_delivery=data['status_delivery']
            status_delivery=1
            # livraison_partielle=data['livraison_partielle']
            livraison_partielle=1
            unitWeightKG=data['unitWeightKG']
        
            vendor_CountryCode=data['vendor_CountryCode']
            vendor_poste=data['vendor_poste']

            

            nb_jours_prevus = abs((date_confirme - date_creation).days)
            nb_jours_dep_fournisseur = abs((date_depart - date_creation).days)


            data = json.dumps({
                'distance': distance,
                'Transport Method': transport_method,
                'Days for shipment (scheduled)': nb_jours_prevus,
                'les jours de depart de fournisseur': nb_jours_dep_fournisseur,
                'Unit Cost (LCY)': unit_cost,
                # 'Vendor_CountryCode': float(vendor_CountryCode),
                # 'vendor_poste': float(vendor_poste),
                'status_delivery':1,
                'Livraison partielle':1,
                'UnitWeightKG':unitWeightKG
            })
            df = pd.json_normalize(data={
                'distance': distance,
                'Transport Method': 1,
                'Days for shipment (scheduled)': nb_jours_prevus,
                'les jours de depart de fournisseur': nb_jours_dep_fournisseur,
                'Unit Cost (LCY)': unit_cost,
                # 'Vendor_CountryCode':float(vendor_CountryCode),
                # 'vendor_poste': float(vendor_poste),
                'status_delivery':1,
                'Livraison partielle':1,
                'UnitWeightKG':unitWeightKG
            })

 
 
          
        
            model = CoreConfig.model 
            result = model.predict(df)
            result = int(result)

            date_livraison = pd.Timestamp(date_creation) + pd.DateOffset(days=result)
            date_livraison=date_livraison.date()

            response_data = json.dumps({"input_data": data, "prediction": [date_livraison.isoformat()]})
            print(response_data)
        return render(
                request, 'result_prediction_date_livrasion.html',
                {'form': form, 'prediction': date_livraison,"unit_cost":unit_cost,"unitWeightKG":unitWeightKG ,"date_creation":date_creation,"date_depart":date_depart,"date_confirme":date_confirme ,"type":type,"distance":distance , "Vendor_CountryCode": vendor_CountryCode, "vendor_poste": vendor_poste}
            )
        








     
# @method_decorator(csrf_exempt, name='dispatch')
@method_decorator(never_cache, name='dispatch')

class QuantityPredictionViewSet(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('core:sing_in')
        form = OrderForm()
        return render(request, 'formulairequantity.html', {'form': form})
    def post(self, request):
        form = OrderForm(request.POST)
        if form.is_valid() == False:
            data = form.cleaned_data
            type_commande = data['type']
            date_creation = pd.to_datetime(data['date_creation'], format='%d/%m/%Y')
            unit_cost = float(request.POST.get('unit_cost'))
            month = date_creation.month
            data = json.dumps({
                'Type': type_commande,
                'Unit Cost (LCY)': unit_cost,
                'month':month,     
            })
            df = pd.json_normalize(data={
                'Type': type_commande,
                'Unit Cost (LCY)': unit_cost,
                'month':month,
            })
            model = CoreConfig.model2 
            result = model.predict(df)
            print(result)
            return render(
                request, 'result_prediction_annomalie.html',
                {'form': form, 'prediction_result': result,"unit_cost":unit_cost ,"date_creation":date_creation ,"type":type_commande }
            )


         


     
from .formulaire import OrderForm

def index(request):

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
                form.save()
            
                return render(request, 'formulaire.html',{'form': form, 'DataOrder':Order.objects.all()})
    else:
        form = OrderForm()
    context = {'form': form}
    return render(request, 'formulaire.html', context)








from django.http import JsonResponse
from .models import Order

def order_data_api(request):
    orders = Order.objects.all()
    
    data = []
    
    for order in orders:
        order_data = {
            'id': order.id,
            'type': order.type,
            'distance': order.distance,
            'transport_method': order.transport_method,
            'vendor_CountryCode': order.vendor_CountryCode,
            'vendor_poste': order.vendor_poste,
            'date_creation': order.date_creation,
            'date_confirme': order.date_confirme,
            'date_depart': order.date_depart,
            'unit_cost': order.unit_cost,
            'unitWeightKG': order.unitWeightKG,
            'status_delivery': order.status_delivery,
            'livraison_partielle': order.livraison_partielle,
            'date_livraison': order.date_livraison,
            'annomalie_stock': order.annomalie_stock,
            'date_livraison_predite': order.date_livraison_predite,
        }
        data.append(order_data)

    return JsonResponse(data, safe=False)












from django.shortcuts import render, redirect
from .models import Order
from django.db.models import F, ExpressionWrapper, fields, Case, When

@never_cache
def valider_livraison(request):
  
    if not request.user.is_authenticated:
        return redirect('core:sing_in')
    
  
    updated_commandes = None 

    if request.method == 'POST':
        commandes_ids = request.POST.getlist('commandes')
        date_livraison = request.POST['date_livraison']

        Order.objects.filter(id__in=commandes_ids, date_livraison__isnull=True).update(date_livraison=date_livraison)

        Order.objects.filter(id__in=commandes_ids, date_livraison__isnull=False).update(
            status_delivery=ExpressionWrapper(
                Case(
                    When(date_livraison__gt=F('date_confirme'), then=1), # Late_time_delivry
                    When(date_livraison=F('date_confirme'), then=2), # On_time_delivry
                    default=0, # Advance_time_delivry
                    output_field=fields.IntegerField()
                ),
                output_field=fields.IntegerField()
            )
        )

        updated_commandes = Order.objects.filter(id__in=commandes_ids)

    commandes = Order.objects.filter(date_livraison__isnull=True)

    return render(request, 'valider_livraison.html', {'commandes': commandes, 'updated_commandes': updated_commandes})










@never_cache
def valider_etat_stock(request):
    
    if not request.user.is_authenticated:
        return redirect('core:sing_in')
    
    if request.method == 'POST':
        commandes_ids = request.POST.getlist('commandes')

        for commande_id in commandes_ids:
            etat_stock = request.POST.get(f'etat_stock_{commande_id}')
            if etat_stock:
                commande = Order.objects.get(id=commande_id)
                commande.etat_stock = etat_stock
                commande.save()

    commandes = Order.objects.filter(etat_stock__isnull=True)
    return render(request, 'valider_etat_stock.html', {'commandes': commandes})











