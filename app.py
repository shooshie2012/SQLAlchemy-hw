import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime
from flask import Flask, jsonify

#db setup
engine = create_engine('sqlite:///resources/hawaii.sqlite')
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

# Flask setup
app = Flask(__name__)

@app.route('/')
def welcome():
    return (
        f'Available Routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/start<br/>'
        f'/api/v1.0/start/end<br/>'
    )

# Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
# Return the JSON representation of your dictionary.
@app.route('/api/v1.0/precipitation')
def precipitation():
    result = session.query(Measurement.date, Measurement.prcp).\
                      order_by(Measurement.date).all()
    precipitation_data = []
    for prcp_data in result:
        prcp_data_dict = {}
        prcp_data_dict['Date'] = prcp_data.date
        prcp_data_dict['Precipitation'] = prcp_data.prcp
        precipitation_data.append(prcp_data_dict)
    return jsonify(precipitation_data)


# Return a JSON list of stations from the dataset.
@app.route('/api/v1.0/stations')
def stations():
    results = session.query(Station).all()
    all_stations = []
    for stations in results:
        stations_dict = {}
        stations_dict['Station'] = stations.station
        stations_dict['Station Name'] = stations.name
        stations_dict['Latitude'] = stations.latitude
        stations_dict['Longitude'] = stations.longitude
        stations_dict['Elevation'] = stations.elevation
        all_stations.append(stations_dict)
    return jsonify(all_stations)

# query for the dates and temperature observations from a year from the last data point.
# Return a JSON list of Temperature Observations (tobs) for the previous year.
@app.route('/api/v1.0/tobs')
def tobs():
    results = session.query(Measurement.station,
                            Measurement.date,
                            Measurement.tobs).\
                      group_by(Measurement.date).\
                      filter(Measurement.date >= 23-8-2016).\
                      order_by(Measurement.station).all()
    temperature_data = []
    for tobs_data in results:
        tobs_data_dict = {}
        tobs_data_dict['Station'] = tobs_data.station
        tobs_data_dict['Date'] = tobs_data.date
        tobs_data_dict['Temperature'] = tobs_data.tobs
        temperature_data.append(tobs_data_dict)
    return jsonify(temperature_data)

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature 
# for a given start or start-end range.

# When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than 
# and equal to the start date.

# When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for 
# dates between the start and end date inclusive.
@app.route("/api/v1.0/<start_date>")
def calc_temps_start(start_date):
    results=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    calc_tobs=[]
    for row in results:
        calc_tobs_dict = {}
        calc_tobs_dict["TMIN"] = row[0]
        calc_tobs_dict["TAVG"] = row[1]
        calc_tobs_dict["TMAX"] = row[2]
        calc_tobs.append(calc_tobs_dict)
    return jsonify(calc_tobs)


@app.route("/api/v1.0/<start_date>/<end_date>")
def calc_temps_start_end(start_date, end_date):
    results=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).all()
    calc_tobs=[]
    for row in results:
        calc_tobs_dict = {}
        calc_tobs_dict["TMIN"] = row[0]
        calc_tobs_dict["TAVG"] = row[1]
        calc_tobs_dict["TMAX"] = row[2]
        calc_tobs.append(calc_tobs_dict)
    return jsonify(calc_tobs)
    return jsonify(result)




if __name__ == '__main__':
    app.run(debug=True)
