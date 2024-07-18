from flask import Flask, render_template, g, request, jsonify
from tables import create_tables, insert_admin, insert_company, insert_location, insert_sensor, insert_sensor_data, update_table, get_table
import sqlite3
from handlers import create_company, create_location, create_sensor, add_sensor_data, get_sensor_data
from database import get_db_connection
from config import DB_NAME

app = Flask(__name__)
app.config['DATABASE'] = DB_NAME

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
    return g.db

@app.route('/')
def index():
    db = get_db()
    create_tables(db)
    db.commit()
    return 'Database initialized and tables created.'

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/insert_admin', methods=['POST'])
def insert_admin_route():
    db = get_db()
    data = request.json
    insert_admin(db, data['username'], data['password'], data['api_key'])
    return 'Admin inserted successfully.'

#--Autenticación de Api Key--#

def verify_company_api_key(api_key):
    db = get_db()
    company = db.execute('SELECT id FROM company WHERE company_api_key = ?', (api_key,)).fetchone()
    return company is not None

def verify_sensor_api_key(api_key):
    db = get_db()
    sensor = db.execute('SELECT id FROM sensor WHERE sensor_api_key = ?', (api_key,)).fetchone()
    return sensor is not None

##--Rutas--##

#--Crear compañías--#
@app.route('/api/v1/companies', methods=['POST'])
def route_create_company():
    return create_company()

#--Listar compañías--#
@app.route('/api/v1/companies', methods=['GET'])
def get_companies():
    db = get_db()
    companies = db.execute('SELECT * FROM company').fetchall()
    return jsonify(companies)

#--Crear ubicación--#
@app.route('/api/v1/locations', methods=['POST'])
def route_create_location():
    data = request.get_json()
    company_api_key = data['company_api_key']
    print(company_api_key)
    if not verify_company_api_key(company_api_key):
        return jsonify({'message': 'Invalid company API key'}), 403
    return create_location()

#--Listar ubicaciones--#
@app.route('/api/v1/locations', methods=['GET'])
def get_locations():
    db = get_db()
    locations = db.execute('SELECT * FROM location').fetchall()
    return jsonify(locations)

#--Crear Sensor--#
@app.route('/api/v1/sensors', methods=['POST'])
def route_create_sensor():
    data = request.get_json()
    company_api_key = data['company_api_key']
    print(company_api_key)
    if not verify_company_api_key(company_api_key):
        return jsonify({'message': 'Invalid company API key'}), 403
    return create_sensor()

#--Listar Sensores--#
@app.route('/api/v1/sensors', methods=['GET'])
def get_sensors():
    db = get_db()
    sensors = db.execute('SELECT * FROM sensor').fetchall()
    return jsonify(sensors)

#--Crear Datos de Sensores--#
@app.route('/api/v1/sensor_data', methods=['POST'])
def route_add_sensor_data():
    data = request.get_json()
    if not verify_sensor_api_key(data['api_key']):
        return jsonify({'message': 'Invalid sensor API key'}), 403
    return add_sensor_data()

#--Listar Datos de Sensores--#
@app.route('/api/v1/sensor_data', methods=['GET'])
def route_get_sensor_data():
    db = get_db()
    sensor_data = db.execute('SELECT * FROM SensorData').fetchall()
    return jsonify(sensor_data)

#--Actualizar Ubicación--#
@app.route('/api/v1/locations/<int:id>', methods=['PUT'])
def update_location(id):
    db = get_db()
    data = request.json
    db.execute('UPDATE location SET company_id = ?, location_name = ?, location_country = ?, location_city = ?, location_meta = ? WHERE id = ?', 
               (data['company_id'], data['location_name'], data['location_country'], data['location_city'], data['location_meta'], id))
    db.commit()
    return jsonify({'message': 'Location updated successfully'})

#--Actualizar Sensor--#
@app.route('/api/v1/sensors/<int:id>', methods=['PUT'])
def update_sensor(id):
    db = get_db()
    data = request.json
    db.execute('UPDATE sensor SET location_id = ?, sensor_name = ?, sensor_category = ?, sensor_meta = ?, sensor_api_key = ? WHERE id = ?', 
               (data['location_id'], data['sensor_name'], data['sensor_category'], data['sensor_meta'], data['sensor_api_key'], id))
    db.commit()
    return jsonify({'message': 'Sensor updated successfully'})

#--Actualizar Dato de Sensor--#
@app.route('/api/v1/sensor_data/<int:id>', methods=['PUT'])
def update_sensor_data(id):
    db = get_db()
    data = request.json
    db.execute('UPDATE sensor_data SET sensor_id = ?, payload = ? WHERE id = ?', 
               (data['sensor_id'], data['payload'], id))
    db.commit()
    return jsonify({'message': 'Sensor data updated successfully'})

#--Eliminar Ubicación--#
@app.route('/api/v1/locations/<int:id>', methods=['DELETE'])
def delete_location(id):
    db = get_db()
    db.execute('DELETE FROM location WHERE id = ?', (id,))
    db.commit()
    return jsonify({'message': 'Location deleted successfully'})

#--Eliminar Sensor--#
@app.route('/api/v1/sensors/<int:id>', methods=['DELETE'])
def delete_sensor(id):
    db = get_db()
    db.execute('DELETE FROM sensor WHERE id = ?', (id,))
    db.commit()
    return jsonify({'message': 'Sensor deleted successfully'})

#--Eliminar Dato de Sensor--#
@app.route('/api/v1/sensor_data/<int:id>', methods=['DELETE'])
def delete_sensor_data(id):
    db = get_db()
    db.execute('DELETE FROM SensorData WHERE id = ?', (id,))
    db.commit()
    return jsonify({'message': 'Sensor data deleted successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
