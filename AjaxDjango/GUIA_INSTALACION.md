# Guía de Instalación - AjaxDjango

Esta guía te ayudará a instalar y configurar la aplicación AjaxDjango paso a paso, incluso si tienes pocos conocimientos de programación.

## Índice

1. [Requisitos Previos](#requisitos-previos)
2. [Descarga del Proyecto](#descarga-del-proyecto)
3. [Instalación de Python y pip](#instalación-de-python-y-pip)
4. [Instalación de Dependencias](#instalación-de-dependencias)
5. [Configuración de Bases de Datos](#configuración-de-bases-de-datos)
6. [Creación de las Tablas](#creación-de-las-tablas)
7. [Ejecución de la Aplicación](#ejecución-de-la-aplicación)
8. [Uso de la Aplicación](#uso-de-la-aplicación)
9. [Solución de Problemas Comunes](#solución-de-problemas-comunes)

## Requisitos Previos

Antes de comenzar, necesitarás:

- Un ordenador con Windows, macOS o Linux
- Conexión a Internet
- Permisos de administrador en tu ordenador
- Al menos uno de estos gestores de bases de datos instalado:
  - MySQL
  - PostgreSQL
  - Oracle
  - SQL Server

## Descarga del Proyecto

1. Visita la página del proyecto en GitHub: [https://github.com/HectorAnchundia/AjaxDjango](https://github.com/HectorAnchundia/AjaxDjango)

2. Haz clic en el botón verde "Code" y selecciona "Download ZIP"

   ![Descarga ZIP](https://i.imgur.com/8vQp8Uh.png)

3. Descomprime el archivo ZIP en una carpeta de tu elección. Por ejemplo, puedes crear una carpeta llamada "Proyectos" en tu escritorio y descomprimirlo allí.

## Instalación de Python y pip

La aplicación está desarrollada en Python, por lo que necesitarás instalarlo:

### Windows

1. Visita [python.org](https://www.python.org/downloads/) y descarga la última versión de Python (3.8 o superior)
2. Ejecuta el instalador descargado
3. **IMPORTANTE**: Marca la casilla "Add Python to PATH" antes de hacer clic en "Install Now"

   ![Instalación Python Windows](https://i.imgur.com/OZYgHVl.png)

4. Completa la instalación siguiendo las instrucciones del asistente

### macOS

1. Si tienes macOS Catalina o posterior, Python ya viene instalado. Puedes verificarlo abriendo Terminal y escribiendo:
   ```
   python3 --version
   ```

2. Si no tienes Python o necesitas una versión más reciente, puedes instalarlo con Homebrew:
   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   brew install python
   ```

### Linux

La mayoría de las distribuciones de Linux ya tienen Python instalado. Puedes verificarlo abriendo Terminal y escribiendo:
```
python3 --version
```

Si no está instalado, puedes instalarlo con el gestor de paquetes de tu distribución:

- Ubuntu/Debian:
  ```
  sudo apt update
  sudo apt install python3 python3-pip
  ```

- Fedora:
  ```
  sudo dnf install python3 python3-pip
  ```

## Instalación de Dependencias

Ahora necesitarás instalar las bibliotecas que requiere la aplicación:

1. Abre una ventana de terminal o símbolo del sistema
2. Navega hasta la carpeta donde descomprimiste el proyecto. Por ejemplo:
   
   ```
   cd C:\Users\TuUsuario\Desktop\Proyectos\AjaxDjango
   ```
   
   o en macOS/Linux:
   
   ```
   cd ~/Desktop/Proyectos/AjaxDjango
   ```

3. Instala las dependencias con pip:
   
   ```
   pip install -r requirements.txt
   ```
   
   o en algunos sistemas:
   
   ```
   pip3 install -r requirements.txt
   ```

4. Espera a que se completen todas las instalaciones. Esto puede tardar unos minutos.

## Configuración de Bases de Datos

La aplicación está configurada para trabajar con diferentes gestores de bases de datos. Necesitarás configurar al menos uno de ellos:

### MySQL

1. Instala MySQL si aún no lo tienes:
   - Windows: Descarga e instala [MySQL Installer](https://dev.mysql.com/downloads/installer/)
   - macOS: `brew install mysql`
   - Linux: `sudo apt install mysql-server` (Ubuntu/Debian)

2. Crea una base de datos llamada `bdproducto`:
   ```sql
   CREATE DATABASE bdproducto;
   ```

3. Asegúrate de que el usuario y la contraseña coincidan con los configurados en `db_performance/settings.py`. Por defecto:
   - Usuario: `root`
   - Contraseña: `1234`

### PostgreSQL

1. Instala PostgreSQL si aún no lo tienes:
   - Windows: Descarga e instala [PostgreSQL Installer](https://www.postgresql.org/download/windows/)
   - macOS: `brew install postgresql`
   - Linux: `sudo apt install postgresql postgresql-contrib` (Ubuntu/Debian)

2. Crea una base de datos llamada `BDPRODUCTO`:
   ```sql
   CREATE DATABASE "BDPRODUCTO";
   ```

3. Asegúrate de que el usuario y la contraseña coincidan con los configurados en `db_performance/settings.py`. Por defecto:
   - Usuario: `postgres`
   - Contraseña: `1234`

### Oracle

1. Instala Oracle Database si aún no lo tienes. Puedes descargar Oracle Database Express Edition (XE) desde el [sitio web de Oracle](https://www.oracle.com/database/technologies/xe-downloads.html)

2. Asegúrate de que el usuario y la contraseña coincidan con los configurados en `db_performance/settings.py`. Por defecto:
   - Usuario: `system`
   - Contraseña: `ORA123`

### SQL Server

1. Instala SQL Server si aún no lo tienes. Puedes descargar SQL Server Express desde el [sitio web de Microsoft](https://www.microsoft.com/es-es/sql-server/sql-server-downloads)

2. Crea una base de datos llamada `BDPRODUCTO`

3. Asegúrate de que el usuario y la contraseña coincidan con los configurados en `db_performance/settings.py`. Por defecto:
   - Usuario: `bd`
   - Contraseña: `1234Aa`

## Creación de las Tablas

Una vez que hayas configurado al menos una base de datos, necesitarás crear las tablas necesarias:

1. Abre una ventana de terminal o símbolo del sistema
2. Navega hasta la carpeta del proyecto
3. Ejecuta los siguientes comandos:

   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

   o en algunos sistemas:

   ```
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```

Estos comandos crearán las tablas necesarias en la base de datos predeterminada (SQLite).

## Ejecución de la Aplicación

Ahora puedes ejecutar la aplicación:

1. En la misma ventana de terminal, ejecuta:

   ```
   python manage.py runserver
   ```

   o en algunos sistemas:

   ```
   python3 manage.py runserver
   ```

2. Verás un mensaje similar a:

   ```
   Starting development server at http://127.0.0.1:8000/
   Quit the server with CONTROL-C.
   ```

3. Abre tu navegador web y accede a la dirección: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

4. ¡Listo! Ahora deberías ver la interfaz de la aplicación AjaxDjango.

## Uso de la Aplicación

Una vez que la aplicación esté en funcionamiento, puedes usarla de la siguiente manera:

1. Completa el formulario de producto con los siguientes datos:
   - Código: Un código único para el producto
   - Nombre: El nombre del producto
   - Precio: El precio del producto (usa punto como separador decimal)
   - Cantidad: La cantidad disponible del producto
   - Fecha: La fecha de registro del producto

2. Selecciona un gestor de base de datos haciendo clic en uno de los botones (MySQL, PostgreSQL, Oracle o SQL Server)

3. La aplicación probará la conexión con la base de datos seleccionada. Si la conexión es exitosa, los botones "Insertar Datos" y "Eliminar Datos" se habilitarán.

4. Haz clic en "Insertar Datos" para iniciar la prueba de inserción. La aplicación insertará datos en la base de datos durante 60 segundos y luego mostrará el número de registros insertados.

5. Haz clic en "Eliminar Datos" si deseas eliminar todos los datos de la tabla.

## Solución de Problemas Comunes

### Error: "No module named 'django'"

**Problema**: Al ejecutar `python manage.py runserver`, aparece un error indicando que no se encuentra el módulo Django.

**Solución**:
1. Asegúrate de haber instalado las dependencias correctamente:
   ```
   pip install -r requirements.txt
   ```
2. Verifica que estás usando la versión correcta de Python:
   ```
   python --version
   ```
   Debería ser 3.8 o superior.

### Error: "Could not find a version that satisfies the requirement..."

**Problema**: Al instalar las dependencias, aparece un error indicando que no se puede encontrar una versión compatible.

**Solución**:
1. Actualiza pip a la última versión:
   ```
   pip install --upgrade pip
   ```
2. Intenta instalar las dependencias nuevamente:
   ```
   pip install -r requirements.txt
   ```

### Error: "OperationalError: (2003, "Can't connect to MySQL server on 'localhost'")"

**Problema**: La aplicación no puede conectarse al servidor MySQL.

**Solución**:
1. Verifica que el servidor MySQL esté en ejecución
2. Comprueba que el usuario y la contraseña en `db_performance/settings.py` sean correctos
3. Asegúrate de que la base de datos `bdproducto` exista
4. Verifica que el puerto 3306 esté abierto y no bloqueado por un firewall

### Error: "OperationalError: FATAL: password authentication failed for user 'postgres'"

**Problema**: La aplicación no puede conectarse al servidor PostgreSQL debido a credenciales incorrectas.

**Solución**:
1. Verifica la contraseña del usuario 'postgres'
2. Actualiza la configuración en `db_performance/settings.py` con la contraseña correcta
3. Reinicia la aplicación

### Error: "Error loading cx_Oracle module: DLL load failed"

**Problema**: No se puede cargar el módulo cx_Oracle para conectarse a Oracle Database.

**Solución**:
1. Asegúrate de tener instalado Oracle Client en tu sistema
2. Descarga e instala Oracle Instant Client desde el [sitio web de Oracle](https://www.oracle.com/database/technologies/instant-client/downloads.html)
3. Agrega la ruta de Oracle Instant Client a tu variable de entorno PATH
4. Reinicia tu terminal y prueba nuevamente

### Error: "Error loading pyodbc module"

**Problema**: No se puede cargar el módulo pyodbc para conectarse a SQL Server.

**Solución**:
1. Instala los controladores ODBC para SQL Server:
   - Windows: Descarga e instala [ODBC Driver for SQL Server](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)
   - macOS: `brew install unixodbc freetds`
   - Linux: `sudo apt install unixodbc-dev tdsodbc`
2. Reinicia tu terminal y prueba nuevamente

### Error: "You have 18 unapplied migration(s)."

**Problema**: Las migraciones no se han aplicado correctamente.

**Solución**:
1. Ejecuta el comando para aplicar las migraciones:
   ```
   python manage.py migrate
   ```

### Error: "Error: That port is already in use."

**Problema**: El puerto 8000 ya está en uso por otra aplicación.

**Solución**:
1. Usa un puerto diferente:
   ```
   python manage.py runserver 8080
   ```
2. Luego accede a la aplicación en: [http://127.0.0.1:8080/](http://127.0.0.1:8080/)

### La aplicación se ejecuta pero no puedo conectarme a ninguna base de datos

**Problema**: Las conexiones a las bases de datos fallan aunque los servicios estén en ejecución.

**Solución**:
1. Verifica que los servicios de base de datos estén en ejecución
2. Comprueba que los usuarios y contraseñas en `db_performance/settings.py` sean correctos
3. Asegúrate de que las bases de datos existan
4. Verifica que no haya firewalls bloqueando las conexiones
5. Intenta conectarte a las bases de datos con otras herramientas para confirmar que funcionan correctamente

### No puedo insertar datos en la base de datos

**Problema**: Al hacer clic en "Insertar Datos", aparece un error o no sucede nada.

**Solución**:
1. Asegúrate de haber completado todos los campos del formulario
2. Verifica que la conexión con la base de datos sea exitosa
3. Comprueba que la tabla `PRODUCTO2` exista en la base de datos
4. Revisa los logs del servidor Django para ver si hay algún error específico
