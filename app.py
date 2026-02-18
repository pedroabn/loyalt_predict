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
Este projeto foi desenvolvido para apoiar a equipe de marketing do Theo na compreensão do público e, principalmente, na recuperação de usuários que já foram mais engajados, mas que se afastaram das plataformas com o tempo.

A análise tem foco especial no grupo de “turistas”, que são usuários com baixa recorrência no momento. A escolha desse recorte é estratégica: já sabemos que, quando um turista é reconquistado, ele tende a retornar ao ciclo e voltar a se comportar como um usuário fiel. Ou seja, atuar sobre esse grupo é uma das formas mais diretas de aumentar retenção e recorrência.
Para viabilizar isso, utilizamos técnicas de análise de dados e Machine Learning para identificar diariamente quais usuários apresentam maior probabilidade de voltar a interagir. Assim, o time de marketing consegue priorizar esforços em pessoas com maior chance de conversão, reduzindo desperdício de ações genéricas e aumentando a eficiência das campanhas.
Como resultado, foi desenvolvido um painel (dashboard) que organiza essas informações de forma simples e visual. Nele, é possível acompanhar:

Top 10 turistas com maior chance de se tornarem fiéis: uma lista diária com os usuários que hoje estão pouco ativos, mas apresentam alta probabilidade de retorno no curto prazo, permitindo ações de reengajamento direcionadas.

Evolução semanal de usuários ativos (WAU): gráficos que mostram a quantidade de usuários ativos por semana e as oscilações ao longo do tempo, ajudando a entender padrões de comportamento e períodos de queda ou retomada.

Variação semanal por ciclo de vida (gráfico em barras): um gráfico que mostra, para cada ciclo de vida (Curioso, Fiel, Turista, etc.), quantos clientes existem na semana atual e como esse volume mudou em relação à semana anterior. Acima de cada coluna, exibimos a variação percentual semanal, permitindo identificar rapidamente quais perfis cresceram (retenção/recuperação) e quais diminuíram (perda ou migração de ciclo). Esse indicador é importante porque evidencia não apenas o tamanho atual de cada grupo, mas também a tendência de movimentação entre os ciclos ao longo do tempo.

Com essas informações, a equipe de marketing passa a atuar com mais estratégia, priorização e foco, aumentando as chances de recuperar usuários que já tiveram histórico de engajamento e transformá-los novamente em fiéis.
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
    st.markdown("""<div class= "subtitle-center"> Recorte para analisar a presença de clientes ativos e em que período do ciclo de vida estão. </div>""", unsafe_allow_html=True)

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
