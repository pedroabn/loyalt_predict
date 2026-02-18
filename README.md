# 📬 Remarketing do TheoMeWhy — Loyalty Predict

Sistema de análise e predição de reengajamento de usuários para a plataforma do **TheoMeWhy**, com foco em identificar **turistas** com alta probabilidade de se tornarem **fiéis** novamente.

---

## 📌 Visão Geral

Este projeto apoia a equipe de marketing na recuperação de usuários que já foram engajados mas se afastaram ao longo do tempo. A iniciativa utiliza técnicas de **Machine Learning** e **análise de dados** para identificar diariamente quais usuários têm maior probabilidade de retornar — permitindo campanhas de reengajamento direcionadas e eficientes.

A lógica central gira em torno dos **ciclos de vida** dos usuários:

| Ciclo | Descrição |
|---|---|
| `01-CURIOSO` | Usuário ativo há 7 dias ou menos (novo) |
| `02-FIEL` | Ativo recentemente com alta recorrência |
| `03-TURISTA` | Última atividade entre 8 e 14 dias atrás |
| `04-DESENCANTADO` | Última atividade entre 15 e 28 dias atrás |
| `05-ZUMBI` | Inativo há mais de 28 dias |
| `06-REBORN` | Retornou após longo período de ausência |
| `07-RECONQUER` | Retornou após ausência moderada |

> O foco do remarketing é o grupo **TURISTA**: usuários com baixa recorrência atual que, quando reconquistados, tendem a retornar ao ciclo de fidelidade.

---

## 🏗️ Arquitetura do Projeto

```
loyaltysystem/
│
├── app.py                          # Dashboard Streamlit
├── requirements.txt                # Dependências Python
├── Makefile                        # Automação de tarefas
│
├── data/
│   ├── loyalty_system/database.db  # Banco de origem (Kaggle)
│   ├── education_platform/database.db
│   ├── analytics/database.db       # Banco analítico (ETL)
│   └── processed/                  # Arquivos intermediários para o app
│       ├── top10_fieis.parquet
│       ├── plot_sau.csv
│       ├── qtd_ciclo.csv
│       ├── meta_ciclo.csv
│       └── dia_venda.csv
│
├── src/
│   ├── eng/
│   │   └── ingestion.py            # Download dos datasets do Kaggle
│   └── analytics/
│       ├── pipeline_analytics.py   # Orquestração do ETL completo
│       ├── exec_query.py           # Executor genérico de queries SQL
│       ├── train.py                # Treinamento do modelo ML
│       ├── PredictFiel.py          # Geração de predições diárias
│       ├── *.sql                   # Queries SQL das tabelas analíticas
│       └── mlruns/                 # Artefatos do MLflow
│
└── st/
    └── plot.py                     # Funções de visualização do Streamlit
```

---

## ⚙️ Pré-requisitos

- Python 3.11+
- Conta no [Kaggle](https://www.kaggle.com/) com credenciais configuradas (`~/.kaggle/kaggle.json`)
- MLflow rodando localmente em `http://localhost:5000`
- Make (opcional, para uso dos atalhos do Makefile)

---

## 🚀 Instalação e Configuração

**1. Clone o repositório:**
```bash
git clone <url-do-repositorio>
cd loyaltysystem
```

**2. Crie e ative o ambiente virtual:**
```bash
python -m venv .venv

# Linux/Mac
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

**3. Instale as dependências:**
```bash
pip install -r requirements.txt
```

Ou usando o Makefile:
```bash
make setup
```

---

## 🔄 Pipeline de Dados

O pipeline é composto por três etapas principais, que podem ser executadas individualmente ou em sequência.

### [1/3] Coleta de Dados

Faz o download dos datasets do Kaggle:
- `teomewhy-loyalty-system` → sistema de pontos e transações
- `teomewhy-education-platform` → dados de cursos e progresso dos alunos

```bash
make collect
# ou
python src/eng/ingestion.py
```

### [2/3] ETL e Feature Engineering

Processa os dados brutos e cria as feature stores no banco analítico (`data/analytics/database.db`). As tabelas geradas incluem:

| Tabela | Descrição |
|---|---|
| `life_cycle` | Classificação diária de ciclo de vida por usuário |
| `fs_transacional` | Features transacionais agregadas (D7, D14, D28, D56, Vida) |
| `fs_educational` | Progresso em cursos por usuário |
| `fs_life_cycle` | Features derivadas do ciclo de vida |
| `fs_all` | Feature store consolidada (input do modelo) |
| `clients` | Perfil de engajamento por canal (email, Twitch, YouTube, etc.) |
| `sau` | Usuários ativos semanais (SAU) |
| `plot_sau` | SAU + quantidade de turistas por semana |
| `meta_ciclo` | Frequência média dos turistas vs. meta |
| `dia_venda` | Dia de pico de compras por semana |
| `qtd_ciclo` | Quantidade de clientes por ciclo de vida + variação semanal |

```bash
make etl
# ou
python src/analytics/pipeline_analytics.py
```

### [3/3] Predições

Carrega o último modelo registrado no MLflow e gera as predições de probabilidade de se tornar fiel para todos os turistas do dia:

```bash
make predict
# ou
python src/analytics/PredictFiel.py
```

O resultado é salvo em `data/processed/top10_fieis.parquet` com os 10 turistas com maior probabilidade de conversão.

---

## 🤖 Modelo de Machine Learning

O modelo é treinado para prever se um usuário **TURISTA** se tornará **FIEL** nos próximos 28 dias (`flFiel`).

**Algoritmo:** `AdaBoostClassifier` com busca de hiperparâmetros via `GridSearchCV`

**Hiperparâmetros explorados:**
- `n_estimators`: [100, 200, 400, 500, 1000]
- `learning_rate`: [0.001, 0.01, 0.05, 0.1, 0.2, 0.5, 0.9, 0.99]

**Pipeline de pré-processamento:**
1. Remoção de features não informativas (`DropFeatures`)
2. Imputação de zeros para features educacionais novas (`github2025`, `python2025`)
3. Imputação categórica para `descLifeCycleD28` ausente → `'Nao-Usuario'`
4. Imputação de 1000 para intervalos de dias sem histórico
5. One-Hot Encoding das variáveis de ciclo de vida

**Métricas de avaliação:** AUC-ROC (treino, teste e OOT — out-of-time)

**Treinar o modelo:**
```bash
make train
# ou
python src/analytics/train.py
```

> ⚠️ O MLflow deve estar rodando antes do treinamento. Use `make mlflow` para iniciá-lo.

**Visualizar experimentos no MLflow:**
```bash
make mlflow
# Acesse: http://localhost:5000
```

---

## 📊 Dashboard

O dashboard é construído com **Streamlit** e exibe:

- **Top 10 Turistas do dia** com maior probabilidade de se tornarem fiéis
- **Métricas semanais:**
  - Meta de frequência média dos turistas atingida
  - Dia de maior venda da semana
  - Dias ativos durante a semana
- **SAU vs. Clientes Turistas** — evolução semanal em gráfico de linha
- **Distribuição por ciclo de vida** — quantidade e variação percentual semanal em gráfico de barras

**Iniciar o app:**
```bash
make app
# ou
streamlit run app.py
```

Acesse em: `http://localhost:8501`

---

## 🛠️ Comandos do Makefile

| Comando | Descrição |
|---|---|
| `make setup` | Cria o ambiente virtual e instala dependências |
| `make setup-dev` | Setup com ferramentas de desenvolvimento (pytest, black, flake8) |
| `make collect` | Baixa os datasets do Kaggle |
| `make etl` | Executa o pipeline de ETL |
| `make predict` | Gera as predições do dia |
| `make train` | Treina o modelo de ML |
| `make mlflow` | Inicia o servidor MLflow UI |
| `make app` | Inicia o dashboard Streamlit |
| `make build` | Pipeline completo: collect → etl → predict |
| `make build-train` | Pipeline completo + treinamento |
| `make run` | Pipeline completo + inicia o app |
| `make clean` | Remove cache Python e artefatos MLflow |
| `make clean-data` | Remove os dados baixados |
| `make clean-all` | Limpeza total (inclui ambiente virtual) |

---

## 🗄️ Bancos de Dados

O projeto utiliza três bancos SQLite:

| Banco | Origem | Conteúdo |
|---|---|---|
| `data/loyalty_system/database.db` | Kaggle | Transações, pontos, clientes |
| `data/education_platform/database.db` | Kaggle | Cursos, episódios, progresso |
| `data/analytics/database.db` | Gerado localmente | Feature stores, modelos de ciclo de vida, tabelas de visualização |

---

## 📦 Principais Dependências

| Biblioteca | Versão | Uso |
|---|---|---|
| `streamlit` | 1.54.0 | Dashboard interativo |
| `plotly` | 6.5.2 | Visualizações |
| `pandas` | ≥2.2.0 | Manipulação de dados |
| `scikit-learn` | 1.8.0 | Modelagem ML |
| `feature-engine` | 1.9.3 | Pré-processamento |
| `mlflow` | 3.9.0 | Rastreamento de experimentos |
| `SQLAlchemy` | 2.0.46 | Conexão com banco de dados |
| `kaggle` | 1.8.3 | Download de datasets |

---

## 👤 Autoria

Projeto criado por **TheoMeWhy** e utilizado para fins educacionais e de demonstração de conhecimento em Engenharia de Dados e Machine Learning.
