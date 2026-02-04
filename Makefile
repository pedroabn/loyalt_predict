# =============================================================================
# Configuração do Projeto
# =============================================================================

# Diretórios
VENV_DIR := .venv
SRC_DIR := src
ENGINEERING_DIR := $(SRC_DIR)/eng
ANALYTICS_DIR := $(SRC_DIR)/analytics

# Configuração específica por sistema operacional
ifeq ($(OS),Windows_NT)
    PYTHON := python
    VENV_PYTHON := $(VENV_DIR)\Scripts\python.exe
    VENV_PIP := $(VENV_DIR)\Scripts\pip.exe
    RM := rmdir /S /Q
    MKDIR := mkdir
    SHELL := cmd.exe
    .SHELLFLAGS := /c
    PATH_SEP := \\
    NULL := nul
else
    PYTHON := python3
    VENV_PYTHON := $(VENV_DIR)/bin/python
    VENV_PIP := $(VENV_DIR)/bin/pip
    RM := rm -rf
    MKDIR := mkdir -p
    PATH_SEP := /
    NULL := /dev/null
endif

# Configuração silenciosa (oculta comandos, mostra apenas logs)
.SILENT:

# =============================================================================
# Targets Principais
# =============================================================================

.DEFAULT_GOAL := help

.PHONY: help
help: ## Exibe esta mensagem de ajuda
	echo.
	echo Comandos disponíveis:
	echo.
	echo   setup           Configura o ambiente virtual e instala dependências
	echo   install         Instala/atualiza apenas as dependências
	echo   upgrade         Atualiza todas as dependências
	echo   collect         Executa scripts de engenharia/coleta de dados
	echo   etl             Executa pipeline de analytics/ETL
	echo   predict         Executa script de predição
	echo   pipeline        Executa apenas o pipeline (sem setup)
	echo   all             Executa todo o pipeline
	echo   lint            Executa linting do código
	echo   format          Formata o código com black
	echo   test            Executa testes
	echo   clean           Remove arquivos temporários e cache
	echo   clean-all       Remove tudo, incluindo ambiente virtual
	echo   show-env        Mostra informações do ambiente
	echo   freeze          Congela dependências atuais
	echo   shell           Abre shell Python no ambiente virtual
	echo.

.PHONY: all
all: setup collect etl predict ## Executa todo o pipeline

# =============================================================================
# Gerenciamento do Ambiente
# =============================================================================

.PHONY: setup
setup: ## Configura o ambiente virtual e instala dependências
	echo [LOG] Removendo ambiente virtual existente...
ifeq ($(OS),Windows_NT)
	-if exist $(VENV_DIR) $(RM) $(VENV_DIR) 2>$(NULL)
else
	-$(RM) $(VENV_DIR) 2>$(NULL)
endif
	echo [LOG] Criando ambiente virtual...
	$(PYTHON) -m venv $(VENV_DIR)
	echo [LOG] Atualizando pip, setuptools e wheel...
	$(VENV_PIP) install --upgrade pip setuptools wheel --quiet
	echo [LOG] Instalando dependências...
	$(VENV_PIP) install -r requirements.txt --quiet
	echo [LOG] Setup concluído com sucesso!

.PHONY: install
install: check-venv ## Instala/atualiza apenas as dependências
	echo [LOG] Instalando dependências...
	$(VENV_PIP) install -r requirements.txt --quiet
	echo [LOG] Instalação concluída!

.PHONY: upgrade
upgrade: check-venv ## Atualiza todas as dependências
	echo [LOG] Atualizando dependências...
	$(VENV_PIP) install --upgrade -r requirements.txt --quiet
	echo [LOG] Atualização concluída!

# =============================================================================
# Pipeline de Dados
# =============================================================================

.PHONY: collect
collect: check-venv ## Executa scripts de engenharia/coleta de dados
	echo [LOG] Iniciando coleta de dados...
ifeq ($(OS),Windows_NT)
	cd $(ENGINEERING_DIR) && $(CURDIR)\$(VENV_PYTHON) ingestion.py
else
	cd $(ENGINEERING_DIR) && $(CURDIR)/$(VENV_PYTHON) ingestion.py
endif
	echo [LOG] Coleta concluída com sucesso!

.PHONY: etl
etl: check-venv ## Executa pipeline de analytics/ETL
	echo [LOG] Iniciando pipeline de analytics...
ifeq ($(OS),Windows_NT)
	cd $(ANALYTICS_DIR) && $(CURDIR)\$(VENV_PYTHON) pipeline_analytics.py
else
	cd $(ANALYTICS_DIR) && $(CURDIR)/$(VENV_PYTHON) ingestion.py
endif
	echo [LOG] ETL concluído com sucesso!

.PHONY: predict
predict: check-venv ## Executa script de predição
	echo [LOG] Iniciando predição...
ifeq ($(OS),Windows_NT)
	cd $(ANALYTICS_DIR) && $(CURDIR)\$(VENV_PYTHON) predict-fiel.py
else
	cd $(ANALYTICS_DIR) && $(CURDIR)/$(VENV_PYTHON) predict-fiel.py
endif
	echo [LOG] Predição concluída com sucesso!

.PHONY: pipeline
pipeline: collect etl predict ## Executa apenas o pipeline (sem setup)
	echo [LOG] Pipeline completo executado com sucesso!

# =============================================================================
# Qualidade de Código
# =============================================================================

.PHONY: lint
lint: check-venv ## Executa linting do código
	echo [LOG] Executando linting...
	-$(VENV_PYTHON) -m flake8 $(SRC_DIR)
	-$(VENV_PYTHON) -m pylint $(SRC_DIR)
	echo [LOG] Linting concluído!

.PHONY: format
format: check-venv ## Formata o código com black
	echo [LOG] Formatando código...
	$(VENV_PYTHON) -m black $(SRC_DIR)
	echo [LOG] Formatação concluída!

.PHONY: test
test: check-venv ## Executa testes
	echo [LOG] Executando testes...
	$(VENV_PYTHON) -m pytest tests/ -v
	echo [LOG] Testes concluídos!

# =============================================================================
# Limpeza
# =============================================================================

.PHONY: clean
clean: ## Remove arquivos temporários e cache
	echo [LOG] Limpando arquivos temporários...
ifeq ($(OS),Windows_NT)
	-for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d" 2>$(NULL)
	-for /d /r . %%d in (*.egg-info) do @if exist "%%d" rmdir /s /q "%%d" 2>$(NULL)
	-for /d /r . %%d in (.pytest_cache) do @if exist "%%d" rmdir /s /q "%%d" 2>$(NULL)
	-del /s /q *.pyc 2>$(NULL)
	-del /s /q *.pyo 2>$(NULL)
else
	-find . -type d -name "__pycache__" -exec $(RM) {} + 2>$(NULL)
	-find . -type f -name "*.pyc" -delete 2>$(NULL)
	-find . -type f -name "*.pyo" -delete 2>$(NULL)
	-find . -type d -name "*.egg-info" -exec $(RM) {} + 2>$(NULL)
	-find . -type d -name ".pytest_cache" -exec $(RM) {} + 2>$(NULL)
endif
	echo [LOG] Limpeza concluída!

.PHONY: clean-all
clean-all: clean ## Remove tudo, incluindo ambiente virtual
	echo [LOG] Removendo ambiente virtual...
ifeq ($(OS),Windows_NT)
	-if exist $(VENV_DIR) $(RM) $(VENV_DIR) 2>$(NULL)
else
	-$(RM) $(VENV_DIR) 2>$(NULL)
endif
	echo [LOG] Limpeza completa concluída!

# =============================================================================
# Utilitários
# =============================================================================

.PHONY: show-env
show-env: check-venv ## Mostra informações do ambiente
	echo [LOG] Informações do ambiente:
	echo.
	$(VENV_PYTHON) --version
	$(VENV_PIP) --version
	echo Virtual env: $(VENV_DIR)
	echo.

.PHONY: freeze
freeze: check-venv ## Congela dependências atuais
	echo [LOG] Congelando dependências...
	$(VENV_PIP) freeze > requirements.txt
	echo [LOG] Dependências salvas em requirements.txt

.PHONY: shell
shell: check-venv ## Abre shell Python no ambiente virtual
	echo [LOG] Abrindo shell Python...
	$(VENV_PYTHON)

# =============================================================================
# Verificações e Dependências
# =============================================================================

.PHONY: check-venv
check-venv:
ifeq ($(OS),Windows_NT)
	@if not exist "$(VENV_DIR)\Scripts\python.exe" ( \
		echo [ERRO] Ambiente virtual não encontrado! && \
		echo [ERRO] Execute: make setup && \
		exit /b 1 \
	)
else
	@if [ ! -f "$(VENV_DIR)/bin/python" ]; then \
		echo "[ERRO] Ambiente virtual não encontrado!"; \
		echo "[ERRO] Execute: make setup"; \
		exit 1; \
	fi
endif