import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save references
Measurement = Base.classes.measurement
Stations = Base.classes.station

# import Flask
from flask import Flask

# Create an app, being sure to pass __name__
app = Flask(__name__)

# Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )


# Define what to do when a user hits the /api/v1.0/precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dicitonary
    precip_data = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict['date'] = date
        precip_dict['prcp'] = prcp
        precip_data.append(precip_dict)
    return jsonify(precip_data)
    
# Define what to do when a user hits the /api/v1.0/stations route
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(Stations.station).all()

    session.close()

    # Create list of stations
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

# Define what to do when a user hits the /api/v1.0/tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    recent_day = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]

    recentDay = dt.datetime.strptime(recent_day, "%Y-%m-%d")

    prevYear = recentDay - dt.timedelta(days=366)

    results = session.query(Measurement.tobs).\
        filter(Measurement.date >= prevYear).\
            filter(Measurement.station == most_active_station).all()
    
    session.close()

    # Create list of tobs
    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs)





if __name__ == "__main__":
    app.run(debug=True)
