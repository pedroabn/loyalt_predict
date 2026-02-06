# Define o diretório do ambiente virtual
VENV_DIR=.venv

ifeq ($(OS),Windows_NT)
    PYTHON=$(VENV_DIR)/Scripts/python.exe
else
    PYTHON=$(VENV_DIR)/bin/python
endif

# Configura o ambiente virtual
$(VENV_DIR):
	python -m venv $(VENV_DIR)
	$(PYTHON) -m pip install --upgrade pip

# Instala dependências
.PHONY: setup
setup: $(VENV_DIR)
	@echo "Verificando dependências..."
	$(PYTHON) -m pip install -r requirements.txt

# Executa os scripts de ingestão
.PHONY: collect
collect: setup
	@echo "--- [1/3] Coletando dados ---"
	$(PYTHON) src/eng/ingestion.py

# ETL das features
.PHONY: etl
etl: setup
	@echo "--- [2/3] Executando ETL ---"
	$(PYTHON) src/analytics/pipeline_analytics.py

# Predição
.PHONY: predict
predict: setup
	@echo "--- [3/3] Executando Predição ---"
	$(PYTHON) src/analytics/PredictFiel.py

# Build completo
.PHONY: build
build: setup collect etl predict

# Rodar streamlit
.PHONY: app
app: setup
	$(PYTHON) -m streamlit run app.py

# Rodar tudo (pipeline + app)
.PHONY: run
run: build app
