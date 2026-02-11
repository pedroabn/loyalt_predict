# Define o diretório do ambiente virtual
VENV_DIR=.venv

# Detecta o sistema operacional e define o caminho do Python
ifeq ($(OS),Windows_NT)
    PYTHON=$(VENV_DIR)/Scripts/python.exe
    PIP=$(VENV_DIR)/Scripts/pip.exe
    RM=cmd /c del /f /q
    RMDIR=cmd /c rmdir /s /q
else
    PYTHON=$(VENV_DIR)/bin/python
    PIP=$(VENV_DIR)/bin/pip
    RM=rm -f
    RMDIR=rm -rf
endif

# ============================================================================
# SETUP E INSTALAÇÃO
# ============================================================================

# Cria o ambiente virtual
$(VENV_DIR):
	@echo "Criando ambiente virtual..."
	python -m venv $(VENV_DIR)
	$(PYTHON) -m pip install --upgrade pip

# Instala dependências
.PHONY: setup
setup: $(VENV_DIR)
	@echo "Instalando dependências..."
	$(PIP) install -r requirements.txt
	@echo "✓ Setup concluído!"

# Instala dependências em modo desenvolvimento
.PHONY: setup-dev
setup-dev: $(VENV_DIR)
	@echo "Instalando dependências de desenvolvimento..."
	$(PIP) install -r requirements.txt
	$(PIP) install pytest black flake8 ipykernel
	@echo "✓ Setup dev concluído!"

# ============================================================================
# DATA PIPELINE
# ============================================================================

# [1/3] Coleta dados dos datasets Kaggle
.PHONY: collect
collect: setup
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "📥 [1/3] Coletando dados do Kaggle..."
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	$(PYTHON) src/eng/ingestion.py
	@echo "✓ Dados coletados com sucesso!"
	@echo ""

# [2/3] Processa ETL e cria feature stores
.PHONY: etl
etl: setup
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "⚙️  [2/3] Executando ETL e Feature Engineering..."
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	$(PYTHON) src/analytics/pipeline_analytics.py
	@echo "✓ ETL concluído com sucesso!"
	@echo ""

# [3/3] Executa predições com modelo treinado
.PHONY: predict
predict: setup
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🤖 [3/3] Gerando predições..."
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	$(PYTHON) src/analytics/PredictFiel.py
	@echo "✓ Predições geradas com sucesso!"
	@echo ""

# ============================================================================
# MACHINE LEARNING
# ============================================================================

# Treina o modelo de ML
.PHONY: train
train: setup
	@echo "🎯 Treinando modelo..."
	$(PYTHON) src/analytics/train.py
	@echo "✓ Modelo treinado!"

# Inicia servidor MLflow
.PHONY: mlflow
mlflow: setup
	@echo "🚀 Iniciando MLflow UI em http://localhost:5000"
	cd src/analytics && $(PYTHON) -m mlflow ui

# ============================================================================
# APLICAÇÃO
# ============================================================================

# Executa a aplicação Streamlit
.PHONY: app
app: setup
	@echo "🌐 Iniciando aplicação Streamlit..."
	$(PYTHON) -m streamlit run app.py

# ============================================================================
# PIPELINES COMPLETOS
# ============================================================================

# Pipeline completo: collect → etl → predict
.PHONY: build
build: collect etl predict
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "✓✓✓ Pipeline completo executado!"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Pipeline completo + treinamento
.PHONY: build-train
build-train: build train
	@echo "✓ Build + Train concluído!"

# Executa tudo e inicia o app
.PHONY: run
run: build
	@echo "🚀 Iniciando aplicação..."
	$(MAKE) app

# ============================================================================
# LIMPEZA
# ============================================================================

# Remove cache Python
.PHONY: clean-cache
clean-cache:
	@echo "🧹 Limpando cache Python..."
	find . -type d -name "__pycache__" -exec $(RMDIR) {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✓ Cache limpo!"

# Remove artefatos MLflow
.PHONY: clean-mlflow
clean-mlflow:
	@echo "🧹 Limpando artefatos MLflow..."
	$(RMDIR) mlartifacts 2>/dev/null || true
	$(RMDIR) mlruns 2>/dev/null || true
	$(RMDIR) src/analytics/mlruns 2>/dev/null || true
	@echo "✓ MLflow limpo!"

# Remove dados baixados
.PHONY: clean-data
clean-data:
	@echo "⚠️  Removendo dados baixados..."
	$(RMDIR) data 2>/dev/null || true
	@echo "✓ Dados removidos!"

# Limpeza completa (exceto venv)
.PHONY: clean
clean: clean-cache clean-mlflow
	@echo "✓ Limpeza completa realizada!"

# Remove tudo incluindo ambiente virtual
.PHONY: clean-all
clean-all: clean clean-data
	@echo "⚠️  Removendo ambiente virtual..."
	$(RMDIR) $(VENV_DIR) 2>/dev/null || true
	@echo "✓ Limpeza total concluída!"