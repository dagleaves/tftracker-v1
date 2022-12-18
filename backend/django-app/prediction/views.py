from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from prediction.apps import PredictionConfig
import pandas as pd

# Create your views here
# Class based view to predict based on IRIS model
class IRIS_Model_Predict(APIView):
    def post(self, request, format=None):
        data = request.data
        keys = []
        values = []
        for key in data:
            keys.append(key)
            values.append(data[key])
        
        response_dict = {"Predicted Iris Species": 1}
        return Response(response_dict, status=200)