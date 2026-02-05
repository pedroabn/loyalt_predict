#%%
import pandas as pd
import sqlalchemy
import mlflow
#%%
con = sqlalchemy.create_engine('sqlite:///../../data/analytics/database.db')
mlflow.set_tracking_uri("http://localhost:5000")

versions = mlflow.search_model_versions(filter_string="name='model_fiel'")
last_version = max((int(i.version) for i in versions))

model = mlflow.sklearn.load_model(f"models:///model_fiel/{last_version}")
data = pd.read_sql("SELECT * FROM fs_all WHERE descLifeFoto = '03-TURISTA'", con)
print(f"Dados carregados: {data.shape}")

# Tudo em 3 linhas:
data['predictFiel'] = model.predict_proba(data[model.feature_names_in_])[:, 3]
data_output = data[['dtRef', 'IdCliente', 'predictFiel']]
    
#%%
data = DBPredict()