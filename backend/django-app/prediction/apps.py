from django.apps import AppConfig
import pandas as pd
from joblib import load
import os

class PredictionConfig(AppConfig):
    name = 'prediction'
    