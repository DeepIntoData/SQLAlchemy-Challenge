from flask import Flask, jsonify, flash
import os
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import numpy as np
import datetime as dt
from datetime import timedelta

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
        f"Welcome to the Home page for SQLAlchemy Challenge<br/>"
        f"To access the data below, please append the following to your link in the address bar<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>" 
        f"/api/v1.0/start/end<br/>"    
        f"<br/>"
        f"INPUT START DATE AND END DATE IN PLACE OF START AND END IN LINK BELOW (YYYY-MM-DD)<br/>"
        f"<br/>"
        f"START/END DATE MUST NOT BE BEFORE 2010-01-01 OR 2017-08-23 AFTER <br/>"  
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

    return jsonify(dict_precip)
    
#STATION LIST
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    print("Server received request for 'Stations' page...")
    station_output = session.query(Station.station,Station.name).all()

    session.close()

    station_list = list(np.ravel(station_output))

    return jsonify(station_list)
     
#TEMPERATURE OBSERVATIONS
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    print("Server received request for 'Temperature' page...")

    last_date = session.query(Measurement.date).\
                order_by(Measurement.date.desc()).\
                first().date

    year_ago = dt.datetime.strptime(last_date, '%Y-%m-%d') - dt.timedelta(days=365)
   
    sta_name = session.query(Measurement.station).\
               group_by(Measurement.station).\
               order_by(func.count(Measurement.station).desc()).\
               filter(Measurement.date>=year_ago).first()

    station = session.query(Measurement.date, Measurement.prcp).\
              order_by(Measurement.date.desc()).\
              filter(Measurement.date>=year_ago, Measurement.station == sta_name[0]).all()
    
    session.close()

    temp_list = list(np.ravel(station))

    return jsonify(temp_list) 

#TEMPERATURE CUSTOMS
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def tobs_custom(start = None, end = None):
    session = Session(engine)
    print("Server received request for 'Start/End' page...")
    
    sel = [func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)]
    
    if not end:
        result = session.query(*sel).filter(Measurement.date >= start).all()
        temp = list(np.ravel(result))    
        
        return jsonify(temp)       

    result = session.query(*sel).filter(Measurement.date >= start).\
             filter(Measurement.date <= end).all()
    temp = list(np.ravel(result))    
    
    return jsonify(temp)      

#----------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
