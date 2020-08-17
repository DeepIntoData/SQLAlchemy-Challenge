from flask import Flask, jsonify
import os
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

os.chdir(os.path.dirname(os.path.abspath(__file__)))

#ENGINE SETUP
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

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
        f"/api/v1.0/<start><br/>" 
        f"/api/v1.0/<start>/<end><br/>"      
    ) 

#PRECIPITATION
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'Precipitation' page...")
    output =    session.query(Measurement.date, func.avg(Measurement.prcp)).\
                group_by(Measurement.date).all()

    dict_precip = dict(output)

    return(
        jsonify(dict_precip)
    )

#STATION LIST
@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'Stations' page...")
    station_select = [Station.station,Station.name]
    select = session.query(*station_select).all()

    station_list = list(select)

    return(
        jsonify(station_list)
    )    

#TEMPERATURE OBSERVATIONS

if __name__ == "__main__":
    app.run(debug=True)
