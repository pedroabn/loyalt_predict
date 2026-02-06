#%%
import pandas as pd
import plotly.express as px
from pathlib import Path
import sqlalchemy

def consql():
# paths
    ROOT_DIR = Path(__file__).resolve().parents[1]  # st -> raiz
    DB_PATH = ROOT_DIR / "data" / "analytics" / "database.db"
    consql = sqlalchemy.create_engine(f"sqlite:///{DB_PATH.as_posix()}")
    return consql

def line_con():
    con = consql()
    df = pd.read_sql("SELECT * FROM plot_Sau WHERE dtRef_week > '2025-06-01'", con)
    df["dtRef_week"] = pd.to_datetime(df["dtRef_week"], errors="coerce")
    df_long = df.melt(
        id_vars="dtRef_week",
        value_vars=["SAU", "qtd_turista"],
        var_name="serie",
        value_name="valor"
    )

    fig = px.line(
        df_long,
        x="dtRef_week",
        y="valor",
        color="serie",
        markers=True,
        color_discrete_map={ #Cores das linhas
            "SAU": "#7C3AED",       
            "qtd_turista": "#2090B5"   
        }
    )

    fig.update_traces(line=dict(width=3))
    fig.update_layout(
        height=400,
        margin=dict(l=10, r=10, t=10, b=10),
        legend_title_text=""
    )
    return fig


def bar_con1():
    con = consql()
    df = pd.read_sql("SELECT * FROM life_cycle WHERE dtRef_week > 2026-01-10 ", con)
    df["dtRef_week"] = pd.to_datetime(df["dtRef_week"], errors="coerce")
    
    g = px.bar(
        df.sort_values("predictFiel", ascending=False).head(10),
        x="IdCliente",
        y="predictFiel",
        text="predictFiel"
    )
    g.update_layout(
        height=350,
        margin=dict(l=10, r=10, t=10, b=10)
    )
    return g