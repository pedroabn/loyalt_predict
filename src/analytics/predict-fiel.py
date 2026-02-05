#%%
import pandas as pd
import sqlalchemy
import mlflow
import streamlit as st
#%%
def DBPredict():
    con = sqlalchemy.create_engine('sqlite:///../../data/analytics/database.db')
    mlflow.set_tracking_uri("http://localhost:5000")

    versions = mlflow.search_model_versions(filter_string="name='model_fiel'")
    last_version = max((int(i.version) for i in versions))

    model = mlflow.sklearn.load_model(f"models:///model_fiel/{last_version}")
    data = pd.read_sql("SELECT * FROM fs_all WHERE descLifeCycleFoto = '03-TURISTA'", con)
    print(f"Dados carregados: {data.shape}")

    # Tudo em 3 linhas:
    data['predictFiel'] = model.predict_proba(data[model.feature_names_in_])[:, 1]
    data_output = data[['dtRef', 'IdCliente', 'predictFiel']]
    data_output['predictFiel'] = round(data_output['predictFiel']*100)
    return data_output
def follow():
    con = sqlalchemy.create_engine('sqlite:///../../data/analytics/database.db')
    data = pd.read_sql("SELECT * FROM clients", con)
    return data

@st.cache_data
def info_flw():
    d = DBPredict()
    f = follow()
    df = d.merge(f, on='IdCliente', how= "left")
    return df
