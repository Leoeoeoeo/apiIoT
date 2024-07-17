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

# @app.route('/insert_company', methods=['POST'])
# def insert_company_route():
#     db = get_db()
#     data = request.json
#     insert_company(db, data['company_name'], data['company_api_key'])
#     return 'Company inserted successfully.'

# @app.route('/insert_location', methods=['POST'])
# def insert_location_route():
#     db = get_db()
#     data = request.json
#     insert_location(db, data['company_id'], data['location_name'], data['location_country'], data['location_city'], data['location_meta'])
#     return 'Location inserted successfully.'

# @app.route('/insert_sensor', methods=['POST'])
# def insert_sensor_route():
#     db = get_db()
#     data = request.json
#     insert_sensor(db, data['location_id'], data['sensor_name'], data['sensor_category'], data['sensor_meta'], data['sensor_api_key'])
#     return 'Sensor inserted successfully.'

# @app.route('/insert_sensor_data', methods=['POST'])
# def insert_sensor_data_route():
#     db = get_db()
#     data = request.json
#     insert_sensor_data(db, data['sensor_id'], data['payload'])
#     return 'Sensor data inserted successfully.'

# @app.route('/update_table', methods=['POST'])
# def update_table_route():
#     db = get_db()
#     data = request.json
#     try:
#         update_table(db, data['table_name'], data['column_name'], data['new_value'], data['condition'])
#         return 'Table updated successfully.'
#     except Exception as e:
#         return f"An error occurred: {e}", 500

# @app.route('/get_table', methods=['GET'])
# def get_table_route():
#     db = get_db()
#     table_name = request.args.get('table_name')
#     data = get_table(db, table_name)
#     return jsonify(data)



def verify_company_api_key(api_key):
    conn = get_db_connection()
    company = conn.execute('SELECT id FROM company WHERE company_api_key = ?', (api_key,)).fetchone()
    conn.close()
    return company

def verify_sensor_api_key(api_key):
    conn = get_db_connection()
    sensor = conn.execute('SELECT id FROM sensor WHERE sensor_api_key = ?', (api_key,)).fetchone()
    conn.close()
    return sensor

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/v1/companies', methods=['POST'])
def route_create_company():
    return create_company()

@app.route('/api/v1/locations', methods=['POST'])
def route_create_location():
    company_api_key = request.headers.get('company_api_key')
    if not verify_company_api_key(company_api_key):
        return jsonify({'message': 'Invalid company API key'}), 403
    return create_location()

@app.route('/api/v1/sensors', methods=['POST'])
def route_create_sensor():
    company_api_key = request.headers.get('company_api_key')
    if not verify_company_api_key(company_api_key):
        return jsonify({'message': 'Invalid company API key'}), 403
    return create_sensor()

@app.route('/api/v1/sensor_data', methods=['POST'])
def route_add_sensor_data():
    data = request.get_json()
    if not verify_sensor_api_key(data['api_key']):
        return jsonify({'message': 'Invalid sensor API key'}), 403
    return add_sensor_data()


@app.route('/api/v1/sensor_data', methods=['GET'])
def route_get_sensor_data():
    company_api_key = request.args.get('company_api_key')
    if not verify_company_api_key(company_api_key):
        return jsonify({'message': 'Invalid company API key'}), 403
    return get_sensor_data()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
