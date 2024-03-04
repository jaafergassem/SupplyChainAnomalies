from django.apps import AppConfig
from django.conf import settings
import joblib
import os




class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    MODEL_FILE = os.path.join(settings.MODELS, "modele3.joblib")
    model = joblib.load(MODEL_FILE)

    MODEL_FILE2 = os.path.join(settings.MODELS2, "modele4.joblib")
    model2 = joblib.load(MODEL_FILE2)


