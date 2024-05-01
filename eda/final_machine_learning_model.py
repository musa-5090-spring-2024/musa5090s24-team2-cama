#import the essential packages
#base packages
import numpy as np
import pandas as pd
import geopandas as gpd
import pathlib

# Plotting packages
import seaborn as sns
from matplotlib import pyplot as plt
import holoviews as hv
import hvplot.pandas

# Sodapy API packages
import requests

# Set a Random Seed
np.random.seed(42)
pd.options.display.max_columns = 999

# Models
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

# Model selection
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV

# Pipelines
from sklearn.pipeline import make_pipeline

# Preprocessing
from sklearn.preprocessing import StandardScaler, PolynomialFeatures


# Import Data
raw_filename ='./opa_properties_raw.csv'
phl_opa_raw = pd.read_csv(raw_filename)

# The feature columns we want to use
cols = [
    "parcel_number",
    "sale_price",
    "total_livable_area",
    "total_area",
    "garage_spaces",
    "fireplaces",
    "number_of_bathrooms",
    "number_of_bedrooms",
    "number_stories",
    "zip_code",
]

# Trim to these columns and remove NaNs
phl_opa = phl_opa_raw[cols].dropna()

# Trim zip code to only the first five digits
phl_opa['zip_code'] = phl_opa['zip_code'].astype(str).str.slice(0, 5)

# Trim very low and very high sales
valid = (phl_opa['sale_price'] > 3000) & (phl_opa['sale_price'] < 1e6)
sales = phl_opa.loc[valid]

# Split the data 70/30
train_set, test_set = train_test_split(sales, test_size=0.3, random_state=42)

# the target labels: log of sale price
y_train = np.log(train_set["sale_price"])
y_test = np.log(test_set["sale_price"])

# The features
feature_cols = [
    "total_livable_area",
    "total_area",
    "garage_spaces",
    "fireplaces",
    "number_of_bathrooms",
    "number_of_bedrooms",
    "number_stories",
    "zip_code"]
X_train = train_set[feature_cols]
X_test = test_set[feature_cols]

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

# Numerical columns
num_cols = [
    "total_livable_area",
    "total_area",
    "garage_spaces",
    "fireplaces",
    "number_of_bathrooms",
    "number_of_bedrooms",
    "number_stories"]

# Categorical columns
cat_cols = ["zip_code"]

# Set up the column transformer with two transformers
# ----> Scale the numerical columns
# ----> One-hot encode the categorical columns

transformer = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), num_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
    ]
)

# Initialize the pipeline
# NOTE: only use 10 estimators here so it will run in a reasonable time
pipe = make_pipeline(
    transformer, RandomForestRegressor(n_estimators=10, 
                                       random_state=42)
)

# Fit the training set
pipe.fit(X_train, y_train);

predictions = pipe.predict(sales[feature_cols])

sales["price_predictions"] = np.exp(predictions)

final_df = sales[["parcel_number","price_predictions"]]

final_df.to_csv("predicted_price.csv")