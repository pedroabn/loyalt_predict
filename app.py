import streamlit as st
import pandas as pd
from st.plot import line_con1, bar_con1, met1, met2, met1_2, met3

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
        - Gráficos sobre o WAU para análise semanal de clientes e variação semanal
        """
    )

# Linha fina separadora
st.markdown('<div class="thin-divider"></div>', unsafe_allow_html=True)

# =========================
# CONTAINER 2 (TABELA)
# =========================
df = pd.read_parquet("data/processed/top10_fieis.parquet")

with st.container():
    st.markdown("### 📄 Previsão de churn dos TURISTAS do dia.")
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


# # =========================
# # CONTAINER 3 (3 BOXES COM MÉTRICAS)
# # =========================

st.markdown("""
<style>
div[data-testid="stMetricValue"] {
    font-weight: 900 !important;
    font-size: 34px !important;
}
div[data-testid="stMetricLabel"] p {
    font-weight: 700 !important;
    font-size: 14px !important;
}
</style>
""", unsafe_allow_html=True)

with st.container(gap='small'):
    c1,c2,c3 = st.columns(3, gap='small')
    with c1:
        m1 = met1()
        m12 = met1_2()
        st.metric(label = "Meta de frequência média atingida", 
                  value= m12, 
                  delta = f"{m1}%")
    with c2:
        b = met2()
        data = pd.to_datetime(b["StarDay"]).strftime("%d/%m/%Y")
        valor = int(b["compras_no_dia"])    
        st.metric(
            label="Data de maior venda da semana, ou anterior:",
            value=f"{data}",
            delta=f"{valor}")
    with c3:
        m3 = met3()
        st.metric(label = 'Dias ativos durante a semana',
                  value = m3)
# # =========================
# # CONTAINER 4 (2 BOXES COM GRÁFICOS)
# # =========================
with st.container(gap="large"):
    st.markdown("""<div class= "title-center"> 📈 Dados da semana </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")

    # --- BARPLOT 1
    with c1:
        st.markdown(""" 
                    <div class="plot-center"> SAU X Clientes Turistas</div>'
                    """, unsafe_allow_html=True)
        g1 = line_con1()
        st.plotly_chart(g1, use_container_width=True)

#     # --- BARPLOT 2
    with c2:
        st.markdown(""" 
                    <div class="plot-center">  Quantidade de alunos por ciclo de vida na semana atual e variação semanal </div>'
                    """, unsafe_allow_html=True)
        g3 = bar_con1()
        st.plotly_chart(g3, use_container_width=True)
