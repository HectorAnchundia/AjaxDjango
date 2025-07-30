"""
Views for the product_app application.
"""
import time
import json
from datetime import datetime, timedelta
from django.shortcuts import render
from django.http import JsonResponse
from django.db import connections
from django.views.decorators.csrf import csrf_exempt
from .models import Producto
from .forms import ProductoForm

def index(request):
    """View for the home page."""
    form = ProductoForm()
    return render(request, 'product_app/index.html', {'form': form})

@csrf_exempt
def test_connection(request):
    """Test database connection."""
    if request.method == 'POST':
        data = json.loads(request.body)
        db_engine = data.get('method')
        
        try:
            # Intentar obtener una conexión a la base de datos
            conn = connections[db_engine]
            conn.cursor()
            return JsonResponse({'status': 1})
        except Exception as e:
            return JsonResponse({'status': 0, 'error': str(e)})
    
    return JsonResponse({'status': 0, 'error': 'Invalid request method'})

@csrf_exempt
def insert_data(request):
    """Insert data into the database for 60 seconds."""
    if request.method == 'POST':
        db_engine = request.GET.get('method')
        
        try:
            # Obtener conexión a la base de datos
            conn = connections[db_engine]
            cursor = conn.cursor()
            
            # Preparar datos para inserción
            data = request.POST.dict()
            
            # Configurar tiempo límite (60 segundos)
            start_time = datetime.now()
            end_time = start_time + timedelta(seconds=60)
            
            # Contador de registros insertados
            counter = 0
            
            # Crear consulta SQL según el motor de base de datos
            if db_engine == 'oracle':
                # Oracle necesita un tratamiento especial para las fechas
                fecha = data.get('fecha')
                fields = ", ".join([f for f in data.keys()])
                placeholders = ", ".join([
                    f"TO_DATE('{data['fecha']}','yyyy-MM-dd')" if k == 'fecha' else f"'{v}'" 
                    for k, v in data.items()
                ])
                sql = f"INSERT INTO PRODUCTO2 ({fields}) VALUES ({placeholders})"
            else:
                # Para otros motores
                fields = ", ".join([f for f in data.keys()])
                placeholders = ", ".join(["%s" for _ in data.keys()])
                sql = f"INSERT INTO PRODUCTO2 ({fields}) VALUES ({placeholders})"
                values = tuple(data.values())
            
            # Insertar datos hasta que se alcance el tiempo límite
            while datetime.now() < end_time:
                if db_engine == 'oracle':
                    cursor.execute(sql)
                else:
                    cursor.execute(sql, values)
                counter += 1
                conn.commit()
            
            return JsonResponse({'status': 1, 'message': f'Registros insertados: {counter}'})
            
        except Exception as e:
            return JsonResponse({'status': 0, 'error': str(e)})
    
    return JsonResponse({'status': 0, 'error': 'Invalid request method'})

@csrf_exempt
def delete_data(request):
    """Delete all data from the database."""
    if request.method == 'POST':
        db_engine = request.GET.get('method')
        
        try:
            # Obtener conexión a la base de datos
            conn = connections[db_engine]
            cursor = conn.cursor()
            
            # Ejecutar la consulta DELETE
            cursor.execute("DELETE FROM PRODUCTO2")
            conn.commit()
            
            return JsonResponse({'status': 1})
        except Exception as e:
            return JsonResponse({'status': 0, 'error': str(e)})
    
    return JsonResponse({'status': 0, 'error': 'Invalid request method'})