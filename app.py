from flask import Flask, g, request, jsonify
from tables import create_tables, insert_admin, insert_company, insert_location, insert_sensor, insert_sensor_data, update_table, get_table
import sqlite3

app = Flask(__name__)
app.config['DATABASE'] = 'instancias/IoT.db'

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

@app.route('/insert_company', methods=['POST'])
def insert_company_route():
    db = get_db()
    data = request.json
    insert_company(db, data['company_name'], data['company_api_key'])
    return 'Company inserted successfully.'

@app.route('/insert_location', methods=['POST'])
def insert_location_route():
    db = get_db()
    data = request.json
    insert_location(db, data['company_id'], data['location_name'], data['location_country'], data['location_city'], data['location_meta'])
    return 'Location inserted successfully.'

@app.route('/insert_sensor', methods=['POST'])
def insert_sensor_route():
    db = get_db()
    data = request.json
    insert_sensor(db, data['location_id'], data['sensor_name'], data['sensor_category'], data['sensor_meta'], data['sensor_api_key'])
    return 'Sensor inserted successfully.'

@app.route('/insert_sensor_data', methods=['POST'])
def insert_sensor_data_route():
    db = get_db()
    data = request.json
    insert_sensor_data(db, data['sensor_id'], data['payload'])
    return 'Sensor data inserted successfully.'

@app.route('/update_table', methods=['POST'])
def update_table_route():
    db = get_db()
    data = request.json
    try:
        update_table(db, data['table_name'], data['column_name'], data['new_value'], data['condition'])
        return 'Table updated successfully.'
    except Exception as e:
        return f"An error occurred: {e}", 500
@app.route('/get_table', methods=['GET'])

def get_table_route():
    db = get_db()
    table_name = request.args.get('table_name')
    data = get_table(db, table_name)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
