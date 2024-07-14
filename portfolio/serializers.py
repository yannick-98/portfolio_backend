from rest_framework import serializers
from .models import ModeloML, Item, HelloWorld

class ModeloMLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModeloML
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

        
class HelloWorldSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelloWorld
        fields = '__all__'





