import flask
import numpy as np
import pandas as pd

#---------- MODELS IN MEMORY ----------------#

import pickled_models

#---------- URLS AND WEB PAGES -------------#

app = flask.Flask(__name__)

@app.route("/")
def viz_page():
    with open("index.html", 'r') as viz_file:
        return viz_file.read()

@app.route("/price", methods=["POST"])
def price():
    data = flask.request.json
    predicted1 = pickled_models.getPrice(data["example"])
    pred_jan = pickled_models.getOccupancy_full(predicted1, data["example"], 'Jan17')
    pred_feb = pickled_models.getOccupancy_full(predicted1, data["example"], 'Feb17')
    pred_mar = pickled_models.getOccupancy_full(predicted1, data["example"], 'Mar17')
    pred_apr = pickled_models.getOccupancy_full(predicted1, data["example"], 'Apr17')
    pred_may = pickled_models.getOccupancy_full(predicted1, data["example"], 'May17')
    pred_jun = pickled_models.getOccupancy_full(predicted1, data["example"], 'Jun17')
    pred_jul = pickled_models.getOccupancy_full(predicted1, data["example"], 'Jul17')
    pred_aug = pickled_models.getOccupancy_full(predicted1, data["example"], 'Aug17')
    pred_sep = pickled_models.getOccupancy_full(predicted1, data["example"], 'Sep17')
    pred_oct = pickled_models.getOccupancy_full(predicted1, data["example"], 'Oct17')
    pred_nov = pickled_models.getOccupancy_full(predicted1, data["example"], 'Nov16')
    pred_dec = pickled_models.getOccupancy_full(predicted1, data["example"], 'Dec16')
    # get occupancy by month:
    predicted3 = [pred_jan, pred_feb, pred_mar, pred_apr, pred_may, pred_jun, pred_jul, pred_aug, pred_sep, pred_oct, pred_nov, pred_dec]
    # get mean occupancy across all months
    predicted2 = np.mean(predicted3)
    # get coordinates
    lat = pickled_models.getCoordinates(data["example"][6])[0]
    lon = pickled_models.getCoordinates(data["example"][6])[1]
    # get polygon array
    polygon = pickled_models.getPolygonCoords(data["example"][6])
    # put together results
    results = {"price": predicted1, "occupancy": predicted2, "calendar": predicted3, "lat": lat, "lon":lon, "polygon_coords": polygon}
    # return json results
    return flask.jsonify(results)

@app.route("/manualPrice", methods=["POST"])
def manualPrice():
    data = flask.request.json
    # predicted1 = pickled_models.getPrice(data["example"])
    predicted1 = data["example"][7]
    # predicted2 = pickled_models.getOccupancy(data["example"])
    pred_jan = pickled_models.getOccupancy_full(predicted1, data["example"], 'Jan17')
    pred_feb = pickled_models.getOccupancy_full(predicted1, data["example"], 'Feb17')
    pred_mar = pickled_models.getOccupancy_full(predicted1, data["example"], 'Mar17')
    pred_apr = pickled_models.getOccupancy_full(predicted1, data["example"], 'Apr17')
    pred_may = pickled_models.getOccupancy_full(predicted1, data["example"], 'May17')
    pred_jun = pickled_models.getOccupancy_full(predicted1, data["example"], 'Jun17')
    pred_jul = pickled_models.getOccupancy_full(predicted1, data["example"], 'Jul17')
    pred_aug = pickled_models.getOccupancy_full(predicted1, data["example"], 'Aug17')
    pred_sep = pickled_models.getOccupancy_full(predicted1, data["example"], 'Sep17')
    pred_oct = pickled_models.getOccupancy_full(predicted1, data["example"], 'Oct17')
    pred_nov = pickled_models.getOccupancy_full(predicted1, data["example"], 'Nov16')
    pred_dec = pickled_models.getOccupancy_full(predicted1, data["example"], 'Dec16')
    # get occupancy by month:
    predicted3 = [pred_jan, pred_feb, pred_mar, pred_apr, pred_may, pred_jun, pred_jul, pred_aug, pred_sep, pred_oct, pred_nov, pred_dec]
    # get mean occupancy across all months
    predicted2 = np.mean(predicted3)
    # get coordinates
    lat = pickled_models.getCoordinates(data["example"][6])[0]
    lon = pickled_models.getCoordinates(data["example"][6])[1]
    # get polygon array
    polygon = pickled_models.getPolygonCoords(data["example"][6])
    # put together results
    results = {"price": predicted1, "occupancy": predicted2, "calendar": predicted3, "lat": lat, "lon":lon, "polygon_coords": polygon}
    # return json results
    return flask.jsonify(results)

#--------- RUN WEB APP SERVER ------------#

# Start the app server on port 80 (the default website port)
app.run(host='0.0.0.0')
app.run(debug=True)

#-----------------------------------------#
