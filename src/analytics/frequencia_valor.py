#%%
from sklearn import cluster, preprocessing
import pandas as pd
import sqlalchemy
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
#%%
def import_query(path):
    with open(path) as open_file:
        query = open_file.read()
    return query

engine_app = sqlalchemy.create_engine("sqlite:///../../data/loyalty_system/database.db")
engine_analytical = sqlalchemy.create_engine("sqlite:///../../data/analytics/database.db")

#%%
query = import_query("life_cycle.sql")

data_especifica = datetime(2026, 1, 20).strftime('%Y-%m-%d')
query = query.format(date=data_especifica)


df = pd.read_sql(query, engine_app)
df.to_sql("life_cycle", engine_analytical, index=False, if_exists="replace")
#%%

############################################
query = import_query('freq.sql')
data = datetime(2026, 1, 20).strftime('%Y-%m-%d')
query = query.format(date=data)
df = pd.read_sql(query, engine_app)
df = df[df['qtdePontosPos'] < 6000]
#%%
plt.plot(df['qtdeFrequencia'], df['qtdePontosPos'], "o")
plt.grid(True)
plt.xlabel("Frequência")
plt.ylabel("Valor")
#%%
minmax = preprocessing.MinMaxScaler()
X = minmax.fit_transform(df[['qtdeFrequencia','qtdePontosPos']])

kmean = cluster.KMeans(n_clusters=5, random_state=42, max_iter=1000)
kmean.fit(X)

df['cluster_calc'] = kmean.labels_
df.groupby(by="cluster_calc")['IdCliente'].count()
#%%
sns.scatterplot(data=df,
                x="qtdeFrequencia",
                y="qtdePontosPos",
                hue="cluster",
                palette="deep")

plt.hlines(y=1500, xmin=0,xmax=25, colors='black')
plt.hlines(y=750, xmin=0,xmax=25, colors='black')
plt.vlines(x=4, ymin=0,ymax=750, colors='black')
plt.vlines(x=10, ymin=0,ymax=6000, colors='black')
plt.grid()
