#---------- PYTHON LIBRARY IMPORTS ----------------#

import pickle
import pandas as pd
import numpy as np
import googlemaps
from math import radians, sin, cos, sqrt, asin

from sklearn.ensemble import GradientBoostingRegressor

import statsmodels.api as sm
from statsmodels.iolib.smpickle import load_pickle

# Import the zipcode-income dictionary
filename_dict = 'input/pickles/zipcode_income.pkl'
with open(filename_dict, 'rb') as handle:
    dictionary_zipcode_income = pickle.load(handle)

# Import the zipcode-coordinates dictionary
filename_coordinates = 'input/pickles/zipcode_coordinates.pkl'
with open(filename_coordinates, 'rb') as coords_handle:
    dictionary_zipcode_coordinates = pickle.load(coords_handle)

# Import the zipcode-distance dictionary
filename_distance = 'input/pickles/zipcode_distance.pkl'
with open(filename_distance, 'rb') as dist_handle:
    dictionary_zipcode_distance = pickle.load(dist_handle)

# Import the zipcode-polygon dictionary
filename_polygons = 'input/pickles/zipcode_polygons.pkl'
with open(filename_polygons, 'rb') as polygon_handle:
    zipcode_polygons = pickle.load(polygon_handle)


# Import the XGB regression (PRICE) model
filename_xgb_model = 'input/pickles/price_regression_model_APP_xgb.sav'
XGB_model = pickle.load(open(filename_xgb_model, 'rb'))


# Import the GLM models for each month
GLM_binomial_Jan17 = load_pickle('input/pickles/GLM_binomial_Jan17.pkl')
GLM_binomial_Feb17 = load_pickle('input/pickles/GLM_binomial_Feb17.pkl')
GLM_binomial_Mar17 = load_pickle('input/pickles/GLM_binomial_Mar17.pkl')
GLM_binomial_Apr17 = load_pickle('input/pickles/GLM_binomial_Apr17.pkl')
GLM_binomial_May17 = load_pickle('input/pickles/GLM_binomial_May17.pkl')
GLM_binomial_Jun17 = load_pickle('input/pickles/GLM_binomial_Jun17.pkl')
GLM_binomial_Jul17 = load_pickle('input/pickles/GLM_binomial_Jul17.pkl')
GLM_binomial_Aug17 = load_pickle('input/pickles/GLM_binomial_Aug17.pkl')
GLM_binomial_Sep17 = load_pickle('input/pickles/GLM_binomial_Sep17.pkl')
GLM_binomial_Oct17 = load_pickle('input/pickles/GLM_binomial_Oct17.pkl')
GLM_binomial_Nov16 = load_pickle('input/pickles/GLM_binomial_Nov16.pkl')
GLM_binomial_Dec16 = load_pickle('input/pickles/GLM_binomial_Dec16.pkl')

def getDistance(zipcode):
    return dictionary_zipcode_distance[distance]

def getCoordinates(zipcode):
    return dictionary_zipcode_coordinates[zipcode]

def getPolygonCoords(zipcode):
    return zipcode_polygons[zipcode]


#---------- ESTIMATOR: PRICE ----------------#

def getPrice(userInput):
    model = XGB_model
    # Find zipcode
    zipcode = userInput[6]
    # use function getIncome to get median_income for zipcode
    income = dictionary_zipcode_income[zipcode]
    # use function getDistance to get distance from NYC from zipcode
    distance = dictionary_zipcode_distance[zipcode]
    # define X
    # X = [accommodates, entire, private, shared, distance, bathrooms, bedrooms, income]
    X = np.matrix([userInput[0], userInput[1], userInput[2], userInput[3], distance, userInput[4], userInput[5], income])
    # use model to predict price for input X
    predicted_price = model.predict(X)
    return max(0, predicted_price[0])


#---------- ESTIMATOR: OCCUPANCY ----------------#

def getOccupancy_full(price, userInput, month):
    if month == 'Jan17':
        GLM_binomial = GLM_binomial_Jan17
    elif month == 'Feb17':
        GLM_binomial = GLM_binomial_Feb17
    elif month == 'Mar17':
        GLM_binomial = GLM_binomial_Mar17
    elif month == 'Apr17':
        GLM_binomial = GLM_binomial_Apr17
    elif month == 'May17':
        GLM_binomial = GLM_binomial_May17
    elif month == 'Jun17':
        GLM_binomial = GLM_binomial_Jun17
    elif month == 'Jul17':
        GLM_binomial = GLM_binomial_Jul17
    elif month == 'Aug17':
        GLM_binomial = GLM_binomial_Aug17
    elif month == 'Sep17':
        GLM_binomial = GLM_binomial_Sep17
    elif month == 'Oct17':
        GLM_binomial = GLM_binomial_Oct17
    elif month == 'Nov16':
        GLM_binomial = GLM_binomial_Nov16
    elif month == 'Dec16':
        GLM_binomial = GLM_binomial_Dec16
    zipcode = userInput[6]
    income = dictionary_zipcode_income[zipcode]
    distance = dictionary_zipcode_distance[zipcode]
    X = np.matrix([1, price, userInput[0], userInput[1], userInput[2], userInput[3], distance, income, userInput[4], userInput[5]])
    predicted_occupancy = GLM_binomial.predict(X).tolist()[0]
    return max(0, predicted_occupancy * 100)
