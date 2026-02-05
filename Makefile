# Define o diretório do ambiente virtual
VENV_DIR=.venv

# Define os diretórios
ENGINEERING_DIR=src/eng
ANALYTICS_DIR=src/analytics

# Configura o ambiente virtual
.PHONY: setup
$(VENV_DIR):
	python -m venv $(VENV_DIR)
	$(VENV_DIR)/Scripts/pip install --upgrade pip

# Instala dependências apenas se requirements.txt mudar ou venv não existir
setup: $(VENV_DIR)
	@echo "Verificando dependências..."
	pip install -r requirements.txt


# Executa os scripts
.PHONY: collect
collect:
	@echo "Ativando ambiente virtual..."
	. $(VENV_DIR)/Scripts/activate
	@echo "Executando scripts de engenharia..."
	cd src/eng && \
	python ingestion.py


# etl das features
.PHONY: etl
etl:
	@echo "Ativando ambiente virtual..."
	. $(VENV_DIR)/Scripts/activate
	@echo "Executando scripts de feature store..."
	cd src/analytics && \
	python pipeline_analytics.py

# predicao
.PHONY: predict
predict:
	@echo "Ativando ambiente virtual..."
	. $(VENV_DIR)/Scripts/activate
	@echo "Executando script de predição..."
	cd src/analytics && \
	python predict-fiel.py


# Alvo padrão
.PHONY: all
all: setup collect etl predict