from flask import Flask, Response, render_template, jsonify
import pandas as pd
from sqlalchemy import create_engine

database = {'user': 'divvy', 
            'password': '1234', 
            'port': '3306',
            'host': 'localhost',
            'database': 'station_activity' }

db_engine = create_engine("""mysql://%s:%s@%s:%s/%s
    """ % (database["user"], database["password"], database["host"], database["port"], database["database"]),
    echo=False)

# Flask "app" Setup
app = Flask(__name__)

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get-data")
def get_data():
    df = pd.read_sql("""
select stationName, latitude, longitude, totalDocks
from stations
    """, db_engine)
    data = df.to_json(orient="records")
    return Response(response=data,status=200,mimetype="application/json")

@app.route("/get-stations")
def get_stations():
    df = pd.read_sql("""
    select name, latitude, longitude, combined
    from station_activity
    """, db_engine)
    data = df.to_json(orient="records")
    return Response(response=data,status=200,mimetype="application/json")


if __name__ == "__main__":
    app.run(debug=True)