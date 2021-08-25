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
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
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

    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= prevYear).\
            filter(Measurement.date <= recentDay).all()
    
    tobs_list = []

    for date, tobs in results:
        tobs_dict = {}
        tobs_dict[date] = tobs
        tobs_list.append(tobs_dict)

    session.close()

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start(start):

    session = Session(engine)

    start_date = session.query(func.min(Measurement.date)).first()[0]
    end_date = session.query(func.max(Measurement.date)).first()[0]

    if start >= start_date and start_date <= end_date:
        temp_calcs = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).filter(Measurement.date <= end_date).all()[0]

        return (
                f"Minimum Temperature: {temp_calcs[0]}</br>"
                f"Average Temperature: {temp_calcs[1]}</br>"
                f"Maximum Temperature: {temp_calcs[2]}"
            )
    else:
        return jsonify(f"Date not found")


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):

    session = Session(engine)

    start_date = session.query(func.min(Measurement.date)).first()[0]
    end_date = session.query(func.max(Measurement.date)).first()[0]

    if start >= start_date and end <= end_date:
        temp_calcs = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).filter(Measurement.date <= end).all()[0]

        return (
                f"Minimum Temperature: {temp_calcs[0]}</br>"
                f"Average Temperature: {temp_calcs[1]}</br>"
                f"Maximum Temperature: {temp_calcs[2]}"
            )

    else:
        return jsonify(f"Date not found")


if __name__ == "__main__":
    app.run(debug=True)
