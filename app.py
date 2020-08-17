from flask import Flask, jsonify, flash
import os
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import numpy as np

os.chdir(os.path.dirname(os.path.abspath(__file__)))

#ENGINE SETUP
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

#FLASK SETUP
app = Flask(__name__)

#HOME PAGE
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return(
        f"Welcome to my 'Home' page!<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>" 
        f"/api/v1.0/start/end<br/>"      
    ) 
#PRECIPITATION
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    print("Server received request for 'Precipitation' page...")
    precip_output =    session.query(Measurement.date, func.avg(Measurement.prcp)).\
                group_by(Measurement.date).all()

    session.close()

    dict_precip = dict(precip_output)

    return(
        jsonify(dict_precip)
    )

#STATION LIST
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    print("Server received request for 'Stations' page...")
    station_output = session.query(Station.station,Station.name).all()

    session.close()

    station_list = list(np.ravel(station_output))

    return(
        jsonify(station_list)
    )    
 

#TEMPERATURE OBSERVATIONS
# @app.route("/api/v1.0/tobs")
# def temperature():
#     session = Session(engine)
#     print("Server received request for 'Temperature' page...")

#     temperature_output = session.query(Measurement.date,Measurement.tobs).all().\
                         
#TEMPERATURE OBSERVATIONS
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature(start = None, end = None):
    session = Session(engine)
    print("Server received request for 'Start/End' page...")
    sel = [func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)]
    
    if not end:
        result = session.query(*sel).filter(Measurement.date >= start).all()
        temp = list(np.ravel(result))    
        #flash("Select Date between")
        return (jsonify(temp))       

    result = session.query(*sel).filter(Measurement.date >= start).\
             filter(Measurement.date <= end).all()
    temp = list(np.ravel(result))    
    #flash("Select Date between")
    return (jsonify(temp))       

if __name__ == "__main__":
    app.run(debug=True)
