import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
measure = Base.classes.measurement
station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def start():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    date_prcp = session.query(measure.date, measure.prcp).all()
    session.close()
    
    all_dates = []
    for date, prcp in date_prcp:
        dict = {}
        dict["date"] = date
        dict["prcp"] = prcp
        all_dates.append(dict)
    return jsonify(all_dates)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(stations.station, stations.name).all()
    session.close()
    
    all_stations = []
    for station, name in results:
        dict = {}
        dict["station"] = station
        dict["name"] = name
        all_stations.append(dict)
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(measure.date, measure.tobs).filter(measure.station == 'USC00519281').all()
    session.close()
    
    all_tobs= []
    for date, tob in results:
        dict = {}
        dict["date"] = date
        dict["tob"] = tob
        all_tobs.append(dict)
    return jsonify(all_tobs)

if __name__ == '__main__':
    app.run(debug=True)

@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    results = session.query(measure.tobs).filter(measure.date >= start).all()
    session.close()
    
    all_tobs= []
    for tob in results:
        dict = {}
        dict["tob"] = tob
        all_tobs.append(dict)
    tob_min = min(all_tobs, key=lambda x:x['tob'])
    tob_max = max(all_tobs, key=lambda x:x['tob'])
    tob_avg = sum(x['tob'] for x in all_tobs) / len(all_tobs)
    summary_tobs = [{"min": tob_min}, {"max": tob_max}, {"average": tob_avg}]
    return jsonify(summary_tobs)

@app.route("/api/v1.0/<start><end>")
def start(start, end):
    session = Session(engine)
    results = session.query(measure.tobs).filter(measure.date >= start).filter(measure.date <= end).all()
    session.close()
    
    all_tobs= []
    for tob in results:
        dict = {}
        dict["tob"] = tob
        all_tobs.append(dict)
    tob_min = min(all_tobs, key=lambda x:x['tob'])
    tob_max = max(all_tobs, key=lambda x:x['tob'])
    tob_avg = sum(x['tob'] for x in all_tobs) / len(all_tobs)
    summary_tobs = [{"min": tob_min}, {"max": tob_max}, {"average": tob_avg}]
    return jsonify(summary_tobs)

if __name__ == '__main__':
    app.run(debug=True)