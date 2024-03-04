from django.urls import path
from rest_framework import routers
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import OrderListCreateView, OrderDetailView



router = routers.DefaultRouter()
router.register(r'users', views.CustomUserViewSet)
router.register(r'groups', views.GroupViewSet)


app_name = 'core'
urlpatterns = [
    path("get-delivery-date-predited/", views.DeliveryDatePredictionViewSet.as_view(), name="delivery-date-prediction"),
    path("get-quantity-predited/", views.QuantityPredictionViewSet.as_view(), name="delivery-quantity-prediction"),
    path("tableaux-prediction/", views.TableauxPredictionView.as_view(), name="tableaux-prediction"),
    path("tableaux-prediction-annomalie/", views.TableauxPredictionAnnomalieView.as_view(), name="tableaux-prediction-annomalie"),
    path('api/order_data/', views.order_data_api, name='order_data_api'),
    path('valider-livraison/', views.valider_livraison, name='valider_livraison'),
    path('valider_etat_stock/', views.valider_etat_stock, name='valider_etat_stock'),

    path('get_commandes_data/', views.get_commandes_data, name='get_commandes_data'),

    path('formulaire/', views.formulaire, name='formulaire'),
    path('resultat/', views.resultat, name='resultat'),

    path('orderform/', views.ajouter_commande, name='orderform'),
    path('list_commandes/', views.lister_commandes, name='list_commandes'),
    path('modifier_commande/<int:id>/', views.modifier_commande, name='modifier_commande'),
    path('supprimer_commande/<int:id>/', views.supprimer_commande, name='supprimer_commande'),


    path('register/', views.sing_up, name='sing_up'),
    path('login/',  views.sing_in, name='sing_in'),
    path('logout/',  views.log_out, name='logout'),  
  
    path('', views.dashboard, name='dashboard')


]

urlpatterns += router.urls


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

