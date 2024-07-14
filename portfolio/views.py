from django.shortcuts import render
from .models import Item
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ModeloML
from .serializers import ModeloMLSerializer, HelloWorldSerializer
import joblib
from django.http import JsonResponse
from .utils import get_pie_chart, getHousePrice
from .scraper import scrape_news

def lista_items(request):
    items = Item.objects.all()
    return render(request, 'mi_aplicacion/lista_items.html', {'items': items})

class PredecirView(APIView):
    def post(self, request):
        serializer = ModeloMLSerializer(data=request.data)
        if serializer.is_valid():
            nombre = serializer.validated_data['nombre']
            modelo_ml = ModeloML.objects.get(nombre=nombre)
            modelo = joblib.load(modelo_ml.archivo_modelo.path)
            datos = request.data.get('datos')
            prediccion = modelo.predict([datos])
            return Response({'prediccion': prediccion[0]}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HelloWorldView(APIView):
    def get(self, request):
        return Response({'message': 'Hello, World!'}, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = HelloWorldSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChartView(APIView):
    def get(self, request):
        chart = get_pie_chart()
        return HttpResponse(chart)


class GetPriceView(APIView):
    def post(self, request):
        return getHousePrice(request)
    
    
class NewsView(APIView):
    def get(self, request):
        query = request.query_params.get('q', None)
        if query is None:
            return Response({'error': 'No search query provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        results = scrape_news(query)
        return Response({'results': results}, status=status.HTTP_200_OK)