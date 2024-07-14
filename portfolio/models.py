from django.db import models


class Item(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class ModeloML(models.Model):
    nombre = models.CharField(max_length=100)
    archivo_modelo = models.FileField(upload_to='modelos/')

    def __str__(self):
        return self.nombre
    

class HelloWorld(models.Model):
    message = models.CharField(max_length=100)
    def __str__(self):
        return self.message
    

class Chart(models.Model):
    data = models.TextField()
    labels = models.TextField()
    colors = models.TextField()
    def __str__(self):
        return self.data
    
class House(models.Model):
    tipo = models.CharField(max_length=100)
    municipio = models.CharField(max_length=100)
    metros = models.IntegerField()
    habitaciones = models.IntegerField()
    garaje = models.BooleanField()
    ascensor = models.BooleanField()
    exterior = models.BooleanField()
    precio = models.IntegerField()
    def __str__(self):
        return self.tipo
    
class News(models.Model):
    headlines = models.TextField()
    def __str__(self):
        return self.headlines
    
    