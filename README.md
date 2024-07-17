# Pasos para iniciar el proyecto

1. Instalar dependencias

- Instalar flask
- Instalar sqlite3

2. Validar versión de Python 3.11 e instalar sqlite en el computador

- Ejecutar el comando `python3 --version`
- Ejecutar el comando `pip install sqlite3`
- Instalar sqllite desde https://www.sqlite.org/2024/sqlite-tools-win-x64-3460000.zip
- - Se abre el sqlite3.exe
- Ejecutar el comando `sqlite3 --version`

3. Iniciar el servidor

- Ejecutar el comando `python app.py`

4. Abrir el navegador y acceder a la ruta `http://localhost:5000/`
5. Rutas disponibles

- `/api/v1/companies`
- `/api/v1/locations`
- `/api/v1/sensors`
- `/api/v1/sensor_data`
- `/`
- - Acá se crean las tablsa en tu sqlite3 base de datos
