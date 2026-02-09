import streamlit as st
import pandas as pd
import altair as alt
from st.plot import line_con, bar_con1, bar_con2

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Remarketing",
    page_icon="✉️",
    layout="wide",
)

# =========================
# CSS (sem borda nos boxes + linha fina)
# =========================
st.markdown(
    """
    <style>
        div[data-testid="stVerticalBlockBorderWrapper"] {
            border: none !important;
            box-shadow: none !important;
            background: transparent !important;
        }

        .thin-divider {
            height: 1px;
            background: rgba(255,255,255,0.12);
            margin: 18px 0 18px 0;
        }

        /* Centralizar título e subtítulo */
        .title-center {
            text-align: center;
            font-size: 44px;
            font-weight: 800;
            margin-bottom: 0px;
        }

        .subtitle-center {
            text-align: center;
            font-size: 18px;
            opacity: 0.75;
            margin-top: 6px;
            margin-bottom: 25px;
        }
        .plot-center {
            text-align: center;
            font-size: 30px;
            margin-top: 6px;
            font-weight: 700;
            margin-bottom: 25px;
        }
        /* Ajuste fino no espaçamento dos gráficos */
        .block-container {
            padding-top: 35px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# DADOS 
# =========================
df = pd.read_parquet("data/processed/top10_fieis.parquet")

# df_line = df.groupby("Data", as_index=False)["Vendas"].sum()

# df_bar_1 = df.groupby("Categoria", as_index=False)["Vendas"].sum()
# df_bar_2 = df.groupby("Categoria", as_index=False)["Lucro"].sum()

# =========================
# HEADER
# =========================
st.markdown('<div class="title-center">✉️ Remarketing do TheoMeWhy</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-center">Sabemos quem pode ser Fiel, mas como atender o público mais propenso de voltar?</div>', unsafe_allow_html=True)

# =========================
# CONTAINER 1 (TEXTO)
# =========================
with st.container():
    st.markdown("### 👋 Bem-vindo!")
    st.write(
        """
        Esse é o projeto baseado no trabalho de pipeline analítico e de ML para a medição da Lealdade do público de Theo.
        Aqui foi projetado um dashboard para o marketing. Com uma produção de ML para o entendimento de como reconquistar o público,
        que um dia já foi atuante dentro das plataformas. Entendemos, por dia, quais usuários são mais propensos de retornar, e colocamos
        um alvo para a equipe de marketing conseguir trazer esse cliente de volta.
        
        Dentro desse dashboard, identificamos alguns dados importantes:
        - Os 10 clientes TURISTAS que podem ser Fieis em um mês
        - Gráficos sobre o WAU para análise semanal de clientes e canais de comunicação ativos
        """
    )

# Linha fina separadora
st.markdown('<div class="thin-divider"></div>', unsafe_allow_html=True)

# =========================
# CONTAINER 2 (TABELA)
# =========================
with st.container():
    st.markdown("### 📄 Previsão de churn dos TURISTAS do dia.")
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

# # =========================
# # CONTAINER 3 (4 BOXS COM GRÁFICOS)
# # =========================
with st.container(gap="large"):
    st.markdown("""<div class= "title-center"> 📈 Visão em gráficos </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")

    # --- BARPLOT 1
    with c1:
        st.markdown(""" 
                    <div class="plot-center"> SAU X Clientes Turistas</div>'
                    """, unsafe_allow_html=True)
        g1 = line_con()
        st.plotly_chart(g1, use_container_width=True)

#     # --- BARPLOT 2
    with c2:
        st.markdown(""" 
                    <div class="plot-center">  Quantidade de alunos por ciclo de vida na semana atual </div>'
                    """, unsafe_allow_html=True)
        g2 =   bar_con1()
        st.plotly_chart(g2, use_container_width=True)
#         st.altair_chart(chart_bar_2, use_container_width=True)

with st.container():
    c3, c4 = st.columns(2, gap="large")
    # --- SCATTERPLOT
    with c3:
        st.markdown("#### Vendas x Lucro")
        g3 = bar_con2()
        st.plotly_chart(g3, use_container_width=True)

    # --- LINE CHART
    with c4:
        st.markdown("#### Evolução diária")
#         chart_line = (
#             alt.Chart(df_line)
#             .mark_line(point=True)
#             .encode(
#                 x=alt.X("Data:T", title=""),
#                 y=alt.Y("Vendas:Q", title=""),
#                 tooltip=["Data", "Vendas"]
#             )
#             .properties(height=240)
#         )
#         st.altair_chart(chart_line, use_container_width=True)
