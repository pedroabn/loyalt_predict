#%%
import streamlit as st
import pandas as pd
from st.plot import line_con1, bar_con1, met2, met1, met1_2, met3
#%%
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
Este projeto foi criado para ajudar a equipe de marketing do Theo a entender melhor o público e trazer de volta aquelas pessoas que antes acompanhavam as plataformas, mas acabaram se afastando.

Usamos técnicas de análise de dados e inteligência artificial para identificar, todos os dias, quais usuários têm mais chances de retornar. Assim, a equipe de marketing pode focar seus esforços nessas pessoas, com ações direcionadas para reconquistá-las de forma mais eficiente.

Desenvolvemos um painel de controle (dashboard) que mostra essas informações de maneira simples e visual. Nele, é possível ver, por exemplo:

    Os 10 clientes que hoje são pouco ativos (chamamos de “turistas”), mas que têm potencial para se tornar fiéis dentro de um mês;

    Gráficos que acompanham a quantidade de usuários ativos por semana (o chamado WAU, ou “Weekly Active Users”), ajudando a entender as variações semanais e o comportamento do público ao longo do tempo.

Com essas informações, o time de marketing consegue agir com mais estratégia e foco, aumentando as chances de trazer de volta quem um dia já foi um usuário engajado.
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
        dfm1 = pd.read_csv('data/processed/meta_ciclo.csv')
        m1 = met1(dfm1)
        m12 = met1_2(dfm1)
        st.metric(label = "Meta de frequência média atingida", 
                  value= m12, 
                  delta = f"{m1}%")
    with c2:
        dfm2 = pd.read_csv('data/processed/dia_venda.csv')
        b = met2(dfm2)
        data = pd.to_datetime(b["StarDay"]).strftime("%d/%m/%Y")
        valor = int(b["compras_no_dia"])    
        st.metric(
            label="Data de maior venda da semana, ou anterior:",
            value=f"{data}",
            delta=f"{valor}")
    with c3:
        dfm3 = pd.read_csv('data/processed/plot_sau.csv')
        m3 = met3(dfm3)
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
        dfg1 = pd.read_csv('data/processed/plot_sau.csv')
        dfg1 = dfg1[dfg1['dtRef_week'] > '2025-08-01']
        g1 = line_con1(dfg1)
        st.plotly_chart(g1, use_container_width=True)

#     # --- BARPLOT 2
    with c2:
        st.markdown(""" 
                    <div class="plot-center">  Quantidade de alunos por ciclo de vida na semana atual e variação semanal </div>'
                    """, unsafe_allow_html=True)
        dfg2 = pd.read_csv('data/processed/qtd_ciclo.csv')
        g2 = bar_con1(dfg2)
        st.plotly_chart(g2, use_container_width=True)
