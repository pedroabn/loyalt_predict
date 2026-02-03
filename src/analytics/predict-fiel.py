import pandas as pd
import sqlalchemy
import mlflow

con = sqlalchemy.create_engine('sqlite:///../../data/analytics/database.db')

mlflow.set_tracking_uri("http://localhost:5000")
#%%