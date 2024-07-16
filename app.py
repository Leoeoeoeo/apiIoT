from flask import Flask, g
from tables import createAdminTable
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
    db.execute('CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, name TEXT)')
    db.execute('INSERT INTO test (name) VALUES ("Hello, World!")')
    createAdminTable(db)
    db.commit()
    return 'Database initialized and data inserted.'

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
