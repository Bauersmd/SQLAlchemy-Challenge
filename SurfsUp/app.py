# Import the dependencies.
import datetime as dt
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Database Setup
#database_path = "../Resources/hawaii.sqlite"
engine = create_engine("sqlite:///C:/Users/SmDai/documents/Sean's Documents/SQLAlchemy-Challenge/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with = engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup
app = Flask(__name__)

# List all the varaibles routes
@app.route("/")
def welcome():
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start_date><br/>"
        f"/api/v1.0/<start_date>/<end_date><br/>"
    )

# Flask Routes
# Routing precipitation the past year(12 months)
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Session Link
    session = Session(engine)
    # Query
    previous_date = dt.date(2017,8,23)-dt.timedelta(days = 365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= previous_date).all()
    session.close()
    #Create dictionary
    prcp_data = []
    for data, prcp in results:
        prcp_dict = {}
        prcp_dict["data"] = data
        prcp_dict["prcp"] = prcp
        prcp_data.append(prcp_dict)
    return jsonify(prcp_data)

# Routing for Station
@app.route("/api/v1.0/station")
def station():
    # Session Link
    session = Session(engine)
    # Query
    results = session.query(Measurement.station).distinct().all()
    session.close()
    # Create dictionary
    station_data = []
    for station in results:
        station_dict = {}
        station_dict["station name"] = station[0]
        station_data.append(station_dict)
    return jsonify(station_data)

# Routing for tobs from the past year
@app.route("/api/v1.0/tobs")
def tobs():
    # Session Link
    session = Session(engine)
    # Query
    previous_date = dt.date(2017,8,23)-dt.timedelta(days = 365)
    results = session.query(Measurement.tobs, Measurement.date).filter((Measurement.station == 'USC00519281') & (Measurement.date >= previous_date)).all()
    session.close()
    # Create Dictionary
    tobs_data = []
    for date, tobs in results: 
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Observation Temperature"] = tobs
        tobs_data.append(tobs_dict)
    return jsonify(tobs_data)

# Routing for min, max, and avg start for temperature
# For Start date please enter '2017-08-23' in the url for this part
@app.route("/api/v1.0/<start_date>")
def temperature_starts(start_date):
    # Session Link
    session = Session(engine)
    # Query
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    temperature_data = []
    for tobs in results:
        temperature_dict = {}
        temperature_dict["Minimum"] = results[0][0]
        temperature_dict["Maximum"] = results[0][1]
        temperature_dict["Average"] = results[0][2]
        temperature_data.append(temperature_dict)
    return jsonify(temperature_data)

# Routing now for start/end date for temperature 
# For Start date please enter '2016-08-23' and end date please enter 2017-08-23 in the url part
@app.route("/api/v1.0/<start_date>/<end_date>")
def temperature_start_end(start_date = None, end_date = None):
    # Session Link
    session = Session(engine)
    # Query
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter((Measurement.date >= start_date)&(Measurement.date <= end_date)).all()
    temperature_data = []
    for tobs in results:
        temperature_dict = {}
        temperature_dict["Minimum"] = results[0][0]
        temperature_dict["Maximum"] = results[0][1]
        temperature_dict["Average"] = results[0][2]
        temperature_data.append(temperature_dict)
    return jsonify(temperature_data)

if __name__ == '__main__':
    app.run(debug=True)
