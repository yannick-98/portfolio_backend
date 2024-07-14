import matplotlib.pyplot as plt
import io
import base64
from django.http import JsonResponse
from django.conf import settings
import pickle
import json
import os
import numpy as np
from sklearn import preprocessing as pre
import pandas as pd

def get_pie_chart():
    # Datos de ejemplo
    generos = ['Acción', 'Comedia', 'Drama', 'Sci-Fi']
    cantidades = [15, 10, 20, 8]

    # Crear el gráfico de pizza
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(cantidades, labels=generos, autopct='%1.1f%%')

    # Cambiar el color del texto de las etiquetas y porcentajes a blanco
    for text in texts:
        text.set_color('white')
    for autotext in autotexts:
        autotext.set_color('white')

    ax.axis('equal')  # Para asegurar que sea un círculo perfecto
    ax.set_title('Average m² price by village', color='white')

    # Convertir el gráfico a una imagen en formato PNG
    buf = io.BytesIO()
    plt.savefig(buf, format='png', transparent=True)
    plt.close(fig)

    # Codificar la imagen en base64 para enviarla como texto
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

    return JsonResponse({'chart_data': image_base64})


def getHousePrice(request):

    municipios_dict = {
    'Aiora': 0, 'Albors': 1, 'Arrancapins': 2, 'Barrio de Favara': 3, 'Benicalap': 4, 'Beniferri': 5, 'Benimaclet': 6, 'Beteró': 7, 'Campanar': 8, 'Camí Fondo': 9, 'Camí Reial': 10, 'Camí de Vera': 11, 'Ciutat Fallera': 12, 'Ciutat Jardí': 13, 'Ciutat Universitària': 14, 'Ciutat de les Arts i de les Ciencies': 15, 'El Botànic': 16, 'El Cabanyal-El Canyamelar': 17, 'El Calvari': 18, 'El Carme': 19, 'El Grau': 20, 'El Mercat': 21, 'El Pilar': 22, 'El Pla del Remei': 23, 'Els Orriols': 24, 'En Corts': 25, 'Exposició': 26, 'Fonteta de Sant Lluìs': 27, 'Gran Vía': 28, 'Jaume Roig': 29, "L'Amistat": 30, "L'Hort de Senabre": 31, "L'Illa Perduda": 32, 'La Carrasca': 33, 'La Creu Coberta': 34, 'La Creu del Grau': 35, 'La Fontsanta': 36, 'La Llum': 37, 'La Petxina': 38, 'La Punta': 39, 'La Raiosa': 40, 'La Roqueta': 41, 'La Seu': 42, 'La Vega Baixa': 43, 'La Xerea': 44, 'Les Tendetes': 45, 'Malilla': 46, 'Marxalenes': 47, 'Mestalla': 48, 'Mont-Olivet': 49, 'Morvedre': 50, 'Na Rovella': 51, 'Natzaret': 52, 'Nou Benicalap': 53, 'Nou Campanar': 54, 'Nou Moles': 55, 'Patraix': 56, 'Penya-Roja': 57, 'Playa de la Malvarrosa': 58, 'Russafa': 59, 'Safranar': 60, 'Sant Antoni': 61, 'Sant Francesc': 62, 'Sant Isidre': 63, 'Sant Llorenç': 64, 'Sant Marcellí': 65, 'Sant Pau': 66, 'Soternes': 67, 'Tormos': 68, 'Torrefiel': 69, 'Tres Forques': 70, 'Trinitat': 71, 'Vara de Quart': 72,}

    def load_model():
        # Cargar el modelo desde el archivo pickle
        pickle_path = os.path.join(settings.BASE_DIR, 'portfolio/house.pickle')
        with open(pickle_path, "rb") as file:
            model = pickle.load(file)

        return model

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print('Datos recibidos:', data)

            # Convertir el nombre del municipio a su número correspondiente
            data['Municipio'] = (municipios_dict[data['Municipio']] + 1)
            print('Municipio num:', data['Municipio'])

            required_fields = ['Tipo', 'Municipio', 'Metros', 'Habitaciones', 'Garaje', 'Ascensor', 'Exterior']
            for field in required_fields:
                if field not in data:
                    raise KeyError(f"Falta el campo requerido: {field}")
                data[field] = int(data[field])

            datos = pd.DataFrame([data])

            print('Datos:', datos)
            print(datos.dtypes)
            
            # Cargar el modelo y el escalador
            model = load_model()
            scaler = pre.StandardScaler()

            # Convertir datos a una matriz bidimensional
            datos = np.array(datos).reshape(1, -1)

            # Escalar los datos de entrada
            datos_scaled = scaler.fit_transform(datos)
            print('Datos escalados:', datos_scaled)

            # Predecir el precio de la casa
            price = model.predict(datos)
            print('Precio predicho:', price)

            return JsonResponse({'price': price[0]})

        except (KeyError, ValueError) as e:
            error_message = f"Error en los datos recibidos: {str(e)}"
            print(error_message)
            return JsonResponse({'error': error_message}, status=400)

        except FileNotFoundError as e:
            error_message = f"Archivo no encontrado: {str(e)}"
            print(error_message)
            return JsonResponse({'error': error_message}, status=500)

        except Exception as e:
            error_message = f"Error interno del servidor: {str(e)}"
            print(error_message)
            return JsonResponse({'error': error_message}, status=500)
    else:
        return JsonResponse({'error': 'Método de solicitud no válido'}, status=405)