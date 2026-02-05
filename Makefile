# Define o diretório do ambiente virtual
VENV_DIR=.venv

# Define o interpretador Python do venv
PYTHON=$(VENV_DIR)/Scripts/python

# Define os diretórios
ENGINEERING_DIR=src/eng
ANALYTICS_DIR=src/analytics

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
	@echo "Executando scripts de engenharia..."
	cd $(ENGINEERING_DIR) && $(CURDIR)/$(PYTHON) ingestion.py

# ETL das features
.PHONY: etl
etl: setup
	@echo "Executando scripts de feature store..."
	cd $(ANALYTICS_DIR) && $(CURDIR)/$(PYTHON) pipeline_analytics.py

# Predição
.PHONY: predict
predict: setup
	@echo "Executando script de predição..."
	cd $(ANALYTICS_DIR) && $(CURDIR)/$(PYTHON) predict-fiel.py

# Limpar ambiente
.PHONY: clean
clean:
	@echo "Removendo ambiente virtual..."
	rm -rf $(VENV_DIR)
	@echo "Removendo arquivos Python cache..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Alvo padrão
.PHONY: all
all: setup collect etl predict