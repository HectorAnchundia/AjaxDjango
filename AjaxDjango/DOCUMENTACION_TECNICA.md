# Documentación Técnica - AjaxDjango

Este documento describe los aspectos técnicos y el funcionamiento interno de la aplicación AjaxDjango, una herramienta para comparar el rendimiento de diferentes gestores de bases de datos.

## Índice

1. [Estructura del Proyecto](#estructura-del-proyecto)
2. [Configuración de Bases de Datos](#configuración-de-bases-de-datos)
3. [Modelos](#modelos)
4. [Formularios](#formularios)
5. [Vistas](#vistas)
6. [URLs](#urls)
7. [Plantillas](#plantillas)
8. [Flujo de Trabajo](#flujo-de-trabajo)

## Estructura del Proyecto

El proyecto está estructurado siguiendo las convenciones de Django:

```
AjaxDjango/
│
├── manage.py                      # Script principal de Django
├── requirements.txt               # Dependencias del proyecto
│
├── db_performance/               # Directorio principal del proyecto Django
│   ├── __init__.py
│   ├── settings.py                # Configuración del proyecto
│   ├── urls.py                    # URLs del proyecto
│   └── wsgi.py                    # Configuración para despliegue
│
├── product_app/                  # Aplicación principal
│   ├── __init__.py
│   ├── admin.py                   # Configuración del admin
│   ├── forms.py                   # Formularios
│   ├── models.py                  # Modelos de datos
│   ├── urls.py                    # URLs de la aplicación
│   └── views.py                   # Vistas y lógica
│
└── templates/                    # Plantillas HTML
    ├── base.html                  # Plantilla base
    └── product_app/
        └── index.html             # Página principal
```

## Configuración de Bases de Datos

La aplicación está configurada para trabajar con múltiples gestores de bases de datos. Esta configuración se encuentra en el archivo `db_performance/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'mysql': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bdproducto',
        'USER': 'root',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '3306',
    },
    'postgres': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'BDPRODUCTO',
        'USER': 'postgres',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '5432',
    },
    'oracle': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'free',
        'USER': 'system',
        'PASSWORD': 'ORA123',
        'HOST': 'localhost',
        'PORT': '1521',
    },
    'sqlserver': {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': 'BDPRODUCTO',
        'USER': 'bd',
        'PASSWORD': '1234Aa',
        'HOST': 'localhost',
        'PORT': '1433',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    },
}
```

Esta configuración permite a la aplicación conectarse a diferentes bases de datos según la selección del usuario.

## Modelos

La aplicación utiliza un único modelo `Producto` definido en `product_app/models.py`:

```python
class Producto(models.Model):
    """
    Model representing a product in the database.
    This model will be used across different database engines.
    """
    codigo = models.CharField(max_length=50, verbose_name="Código")
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    cantidad = models.IntegerField(verbose_name="Cantidad")
    fecha = models.DateField(verbose_name="Fecha")

    class Meta:
        db_table = 'PRODUCTO2'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
```

Este modelo define la estructura de la tabla `PRODUCTO2` que se utilizará en todas las bases de datos.

## Formularios

El formulario para crear productos está definido en `product_app/forms.py`:

```python
class ProductoForm(forms.ModelForm):
    """Form for creating and updating Producto objects."""
    
    class Meta:
        model = Producto
        fields = ['codigo', 'nombre', 'precio', 'cantidad', 'fecha']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
```

Este formulario se utiliza para recopilar los datos del producto que se insertarán en la base de datos.

## Vistas

Las vistas de la aplicación están definidas en `product_app/views.py`. Las principales funciones son:

### Vista principal (index)

```python
def index(request):
    """View for the home page."""
    form = ProductoForm()
    return render(request, 'product_app/index.html', {'form': form})
```

Esta vista simplemente renderiza la página principal con el formulario.

### Prueba de conexión

```python
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
```

Esta vista prueba la conexión con la base de datos seleccionada y devuelve un resultado JSON.

### Inserción de datos

```python
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
```

Esta vista inserta datos en la base de datos seleccionada durante 60 segundos y devuelve el número de registros insertados.

### Eliminación de datos

```python
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
```

Esta vista elimina todos los datos de la tabla `PRODUCTO2` en la base de datos seleccionada.

## URLs

Las URLs de la aplicación están definidas en `product_app/urls.py`:

```python
urlpatterns = [
    path('', views.index, name='index'),
    path('api/test-connection/', views.test_connection, name='test_connection'),
    path('api/insert/', views.insert_data, name='insert_data'),
    path('api/delete/', views.delete_data, name='delete_data'),
]
```

Estas URLs definen los puntos de entrada para las diferentes funcionalidades de la aplicación.

## Plantillas

La aplicación utiliza dos plantillas principales:

### Plantilla base (base.html)

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Comparación de Velocidad de Gestores de BD{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11.6.15/dist/sweetalert2.all.min.js"></script>
    {% block extra_css %}{% endblock %}
</head>
<body>
    <div class="container mt-4">
        {% block content %}{% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

Esta plantilla define la estructura básica de todas las páginas de la aplicación.

### Plantilla principal (index.html)

La plantilla principal contiene el formulario, los botones para seleccionar la base de datos y los botones para realizar las operaciones. También incluye el código JavaScript para manejar las interacciones con el usuario.

El código JavaScript más relevante incluye:

#### Prueba de conexión

```javascript
function testConnection(method) {
    $("#results").html("<p>Probando conexión con " + method + "...</p>");
    
    $.ajax({
        url: "{% url 'test_connection' %}",
        type: "POST",
        data: JSON.stringify({ method: method }),
        contentType: "application/json",
        success: function(response) {
            if (response.status === 1) {
                $("#results").html("<p class='text-success'>Conexión exitosa con " + method + ".</p>");
                $("#btnInsert, #btnDelete").prop("disabled", false);
            } else {
                $("#results").html("<p class='text-danger'>Error de conexión con " + method + ": " + response.error + "</p>");
                $("#btnInsert, #btnDelete").prop("disabled", true);
            }
        },
        error: function(xhr, status, error) {
            $("#results").html("<p class='text-danger'>Error de conexión: " + error + "</p>");
            $("#btnInsert, #btnDelete").prop("disabled", true);
        }
    });
}
```

#### Inserción de datos

```javascript
$("#btnInsert").click(function() {
    if (!selectedMethod) {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Seleccione un gestor de base de datos primero'
        });
        return;
    }

    // Validar formulario
    let isValid = true;
    $("#productForm input").each(function() {
        if ($(this).val() === "") {
            isValid = false;
            return false;
        }
    });

    if (!isValid) {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Complete todos los campos del formulario'
        });
        return;
    }

    // Mostrar mensaje de carga
    Swal.fire({
        title: 'Insertando datos...',
        html: 'Este proceso tomará 60 segundos',
        allowOutsideClick: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });

    // Enviar datos
    $.ajax({
        url: "{% url 'insert_data' %}?method=" + selectedMethod,
        type: "POST",
        data: $("#productForm").serialize(),
        success: function(response) {
            Swal.close();
            if (response.status === 1) {
                Swal.fire({
                    icon: 'success',
                    title: 'Éxito',
                    text: response.message
                });
                $("#results").html("<p class='text-success'>" + response.message + "</p>");
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'Error al insertar datos: ' + response.error
                });
                $("#results").html("<p class='text-danger'>Error al insertar datos: " + response.error + "</p>");
            }
        },
        error: function(xhr, status, error) {
            Swal.close();
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Error al insertar datos: ' + error
            });
            $("#results").html("<p class='text-danger'>Error al insertar datos: " + error + "</p>");
        }
    });
});
```

#### Eliminación de datos

```javascript
$("#btnDelete").click(function() {
    if (!selectedMethod) {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Seleccione un gestor de base de datos primero'
        });
        return;
    }

    // Confirmar eliminación
    Swal.fire({
        title: '¿Está seguro?',
        text: "Se eliminarán todos los datos de la tabla PRODUCTO2",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            // Mostrar mensaje de carga
            Swal.fire({
                title: 'Eliminando datos...',
                allowOutsideClick: false,
                didOpen: () => {
                    Swal.showLoading();
                }
            });

            // Enviar solicitud de eliminación
            $.ajax({
                url: "{% url 'delete_data' %}?method=" + selectedMethod,
                type: "POST",
                success: function(response) {
                    Swal.close();
                    if (response.status === 1) {
                        Swal.fire({
                            icon: 'success',
                            title: 'Éxito',
                            text: 'Datos eliminados correctamente'
                        });
                        $("#results").html("<p class='text-success'>Datos eliminados correctamente</p>");
                    } else {
                        Swal.fire({
                            icon: 'error',
                            title: 'Error',
                            text: 'Error al eliminar datos: ' + response.error
                        });
                        $("#results").html("<p class='text-danger'>Error al eliminar datos: " + response.error + "</p>");
                    }
                },
                error: function(xhr, status, error) {
                    Swal.close();
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: 'Error al eliminar datos: ' + error
                    });
                    $("#results").html("<p class='text-danger'>Error al eliminar datos: " + error + "</p>");
                }
            });
        }
    });
});
```

## Flujo de Trabajo

El flujo de trabajo de la aplicación es el siguiente:

1. El usuario accede a la página principal (`/`).
2. El usuario completa el formulario con los datos del producto.
3. El usuario selecciona un gestor de base de datos (MySQL, PostgreSQL, Oracle o SQL Server).
4. La aplicación prueba la conexión con la base de datos seleccionada.
5. Si la conexión es exitosa, el usuario puede:
   - Insertar datos durante 60 segundos.
   - Eliminar todos los datos de la tabla.
6. La aplicación muestra los resultados de las operaciones.

Este flujo permite al usuario comparar el rendimiento de diferentes gestores de bases de datos en términos de velocidad de inserción de datos.