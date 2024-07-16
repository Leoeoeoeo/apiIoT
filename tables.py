def create_tables(db):
    db.execute('''
        CREATE TABLE IF NOT EXISTS Admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(100) NOT NULL,
            password VARCHAR(100) NOT NULL,
            api_key VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    db.execute('''
        CREATE TABLE IF NOT EXISTS Company (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name VARCHAR(100) NOT NULL,
            company_api_key VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    db.execute('''
        CREATE TABLE IF NOT EXISTS Location (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER,
            location_name VARCHAR(100) NOT NULL,
            location_country VARCHAR(100) NOT NULL,
            location_city VARCHAR(100) NOT NULL,
            location_meta VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (company_id) REFERENCES Company(id)
        )
    ''')
    db.execute('''
        CREATE TABLE IF NOT EXISTS Sensor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location_id INTEGER,
            sensor_name VARCHAR(100) NOT NULL,
            sensor_category VARCHAR(100) NOT NULL,
            sensor_meta VARCHAR(100),
            sensor_api_key VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (location_id) REFERENCES Location(id)
        )
    ''')
    db.execute('''
        CREATE TABLE IF NOT EXISTS SensorData (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id INTEGER,
            payload TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sensor_id) REFERENCES Sensor(id)
        )
    ''')
    db.commit()
def insert_admin(db, username, password, api_key):
    db.execute('''
        INSERT INTO Admin (username, password, api_key)
        VALUES (?, ?, ?)
    ''', (username, password, api_key))
    db.commit()

def insert_company(db, company_name, company_api_key):
    db.execute('''
        INSERT INTO Company (company_name, company_api_key)
        VALUES (?, ?)
    ''', (company_name, company_api_key))
    db.commit()

def insert_location(db, company_id, location_name, location_country, location_city, location_meta):
    db.execute('''
        INSERT INTO Location (company_id, location_name, location_country, location_city, location_meta)
        VALUES (?, ?, ?, ?, ?)
    ''', (company_id, location_name, location_country, location_city, location_meta))
    db.commit()

def insert_sensor(db, location_id, sensor_name, sensor_category, sensor_meta, sensor_api_key):
    db.execute('''
        INSERT INTO Sensor (location_id, sensor_name, sensor_category, sensor_meta, sensor_api_key)
        VALUES (?, ?, ?, ?, ?)
    ''', (location_id, sensor_name, sensor_category, sensor_meta, sensor_api_key))
    db.commit()

def insert_sensor_data(db, sensor_id, payload):
    db.execute('''
        INSERT INTO SensorData (sensor_id, payload)
        VALUES (?, ?)
    ''', (sensor_id, payload))
    db.commit()

def update_table(db, table_name, column_name, new_value, condition):
    try:
        query = f'UPDATE {table_name} SET {column_name} = ? WHERE {condition}'
        db.execute(query, (new_value,))
        db.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        raise
    except Exception as e:
        print(f"Exception in update_table: {e}")
        raise

def get_table(db, table_name):
    cursor = db.execute(f'''
        SELECT * FROM {table_name}
    ''')
    return cursor.fetchall()
