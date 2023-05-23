from flask import Flask
import psycopg2

app = Flask(__name__)
conn = psycopg2.connect(dbname="nom_de_la_base_de_donnees", user="utilisateur", password="mot_de_passe", host="localhost")

@app.before_first_request
def setup():
    with app.open_resource('schema.sql', mode='r') as f:
        conn.cursor().execute(f.read())
        conn.commit()
