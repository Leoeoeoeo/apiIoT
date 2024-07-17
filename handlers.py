from flask import request, jsonify
from database import get_db_connection
import uuid

def create_company():
    data = request.get_json()
    company_api_key = str(uuid.uuid4())
    conn = get_db_connection()
    conn.execute('INSERT INTO company (company_name, company_api_key) VALUES (?, ?)',
                 (data['company_name'], company_api_key))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Company created', 'company_api_key': company_api_key}), 201

def create_location():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('INSERT INTO location (company_id, location_name, location_country, location_city, location_meta) VALUES (?, ?, ?, ?, ?)',
                 (data['company_id'], data['location_name'], data['location_country'], data['location_city'], data.get('location_meta')))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Location created'}), 201

def create_sensor():
    data = request.get_json()
    sensor_api_key = str(uuid.uuid4())
    conn = get_db_connection()
    conn.execute('INSERT INTO sensor (location_id, sensor_name, sensor_category, sensor_meta, sensor_api_key) VALUES (?, ?, ?, ?, ?)',
                 (data['location_id'], data['sensor_name'], data['sensor_category'], data.get('sensor_meta'), sensor_api_key))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Sensor created', 'sensor_api_key': sensor_api_key}), 201

def add_sensor_data():
    data = request.get_json()
    conn = get_db_connection()
    sensor = conn.execute('SELECT id FROM sensor WHERE sensor_api_key = ?', (data['api_key'],)).fetchone()
    if not sensor:
        return jsonify({'message': 'Invalid sensor API key'}), 400
    for entry in data['json_data']:
        conn.execute('INSERT INTO sensor_data (sensor_id, data) VALUES (?, ?)',
                     (sensor['id'], str(entry)))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Data added'}), 201

def get_sensor_data():
    company_api_key = request.args.get('company_api_key')
    from_time = request.args.get('from')
    to_time = request.args.get('to')
    sensor_ids = request.args.getlist('sensor_id')

    conn = get_db_connection()
    company = conn.execute('SELECT id FROM company WHERE company_api_key = ?', (company_api_key,)).fetchone()
    if not company:
        return jsonify({'message': 'Invalid company API key'}), 400

    query = 'SELECT * FROM sensor_data WHERE sensor_id IN ({}) AND timestamp BETWEEN ? AND ?'.format(
        ','.join('?' for _ in sensor_ids))
    params = sensor_ids + [from_time, to_time]
    data = conn.execute(query, params).fetchall()
    conn.close()

    result = [{'sensor_id': d['sensor_id'], 'data': d['data'], 'timestamp': d['timestamp']} for d in data]
    return jsonify(result), 200
