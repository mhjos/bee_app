from flask import Flask, render_template, session
from config import Config
from models import db
from routes import init_routes

import time
import pymysql

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY  # make sure you have a secret key set

# Initialize database
db.init_app(app)

# Retry connecting to DB
with app.app_context():
    retries = 10
    while retries > 0:
        try:
            db.create_all()
            print("Database connected!")
            break
        except pymysql.err.OperationalError:
            print("Waiting for DB...")
            time.sleep(3)
            retries -= 1
    else:
        raise Exception("Cannot connect to the database")

# # Create tables (Hive + Bee)
# with app.app_context():
#     db.create_all()

# Initialize API routes
init_routes(app)

# ---- Front-end pages ----
@app.route('/')
def launch():
    return render_template('index.html')

@app.route('/bee_stat')
def bee_stat():
    # Redirect to index if no bee logged in
    if 'bee_id' not in session:
        return render_template('index.html')
    return render_template('bee_stat.html')

@app.route('/list_hives')
def list_hives_page():
    if 'bee_id' not in session:
        return render_template('index.html')
    return render_template('list_hives.html')

@app.route('/hive_stat')
def hive_stat():
    if 'bee_id' not in session:
        return render_template('index.html')
    return render_template('hive_stat.html')

# Optional: route to get current bee info for front-end JS
@app.route('/current_bee')
def current_bee():
    if 'bee_id' in session:
        return {
            'id': session['bee_id'],
            'name': session['bee_name'],
            'pollen': session.get('bee_pollen', 0)
        }, 200
    return {'error': 'No bee logged in'}, 404

if __name__ == "__main__":
    app.run(debug=True)
