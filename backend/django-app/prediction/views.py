from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from prediction.apps import PredictionConfig
import pandas as pd

# Create your views here
# Class based view to predict based on IRIS model
class IRIS_Model_Predict(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None):
        data = request.data
        keys = []
        values = []
        for key in data:
            keys.append(key)
            values.append(data[key])
        
        response_dict = {"Predicted Iris Species": 1}
        return Response(response_dict, status=200)