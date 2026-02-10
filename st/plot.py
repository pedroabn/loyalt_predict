#%%
import pandas as pd
import plotly.express as px
from pathlib import Path
import sqlalchemy
import plotly.graph_objects as go

def consql():
# paths
    ROOT_DIR = Path(__file__).resolve().parents[1]  # st -> raiz
    DB_PATH = ROOT_DIR / "data" / "analytics" / "database.db"
    consql = sqlalchemy.create_engine(f"sqlite:///{DB_PATH.as_posix()}")
    return consql

def line_con1():
    con = consql()
    df = pd.read_sql("SELECT * FROM plot_Sau WHERE dtRef_week > '2025-08-01'", con)
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
            "SAU": "#2090B5",       
            "qtd_turista": "#4A12A9"   
        }
    )

    fig.update_traces(line=dict(width=3))
    fig.update_layout(
        height=400,
        margin=dict(l=10, r=10, t=10, b=10),
        legend_title_text=""
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    return fig



def bar_con1():
    con = consql()
    df = pd.read_sql("SELECT * FROM qtd_ciclo", con)

    df["qtd"] = pd.to_numeric(df["qtd"], errors="coerce")
    df["var_perc"] = pd.to_numeric(df["var_perc"], errors="coerce")

    df = df.sort_values("qtd", ascending=False).reset_index(drop=True)

    # label do texto
    df["var_perc_txt"] = (df["var_perc"] / 100).map("{:.0%}".format)

    # cor do texto (verde/vermelho)
    df["txt_color"] = df["var_perc"].apply(lambda x: "#22C55E" if x > 0 else "#EF4444")

    # cores das barras por tipo
    tipo_colors = {
        "01-CURIOSO": "#97D1E4",
        "02-FIEL": "#97D1E4",
        "03-TURISTA": "#4A12A9",
        "04-DESENCANTADO": "#97D1E4",
        "06-REBORN": "#97D1E4",
        "07-RECONQUER": "#97D1E4",
    }
    df["bar_color"] = df["tipo"].map(tipo_colors).fillna("#97D1E4")

    # x numérico (isso evita problema de posição)
    df["xpos"] = df.index

    fig = go.Figure()

    # barras
    fig.add_trace(
        go.Bar(
            x=df["xpos"],
            y=df["qtd"],
            marker=dict(color=df["bar_color"]),
            hovertext=df["tipo"],
            hovertemplate="<b>%{hovertext}</b><br>qtd=%{y}<extra></extra>",
        )
    )

    # annotations (texto colorido por barra)
    for i, row in df.iterrows():
        fig.add_annotation(
            x=row["xpos"],
            y=row["qtd"],
            text=row["var_perc_txt"],
            showarrow=False,
            yshift=14,
            font=dict(size=14, color=row["txt_color"]),
        )

    # eixo x com labels (tipo)
    fig.update_layout(
        height=400,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(
            tickmode="array",
            tickvals=df["xpos"],
            ticktext=df["tipo"],
            title="",
        ),
        yaxis=dict(title="qtd"),
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    return fig

def met1():
    con = consql()
    df = pd.read_sql("SELECT * FROM meta_ciclo", con)
    m = df.sort_values('dtRef_week', ascending=False)
    m = m['Meta_Percentual'].head(1).values[0]
    return m

# def met2():
#     con = consql()
#     df = pd.read_sql("SELECT * FROM qtd_ciclo", con)
    
#     m =
#     return m

# def met3():
#     con = consql()
#     df = pd.read_sql("SELECT * FROM qtd_ciclo", con)
#     m =
#     return m