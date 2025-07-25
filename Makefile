# Makefile
# Comandos úteis para o desenvolvimento

.PHONY: help build run-dev run-prod stop clean test logs

help: ## Mostrar comandos disponíveis
	@grep -E '^[a-zA-Z_-]+:.*?## .*$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $1, $2}'

build: ## Build da imagem Docker
	docker-compose build

run-dev: ## Executar em modo desenvolvimento
	docker-compose -f docker-compose.dev.yml up --build

run-prod: ## Executar em modo produção
	docker-compose up -d --build

stop: ## Parar os containers
	docker-compose down
	docker-compose -f docker-compose.dev.yml down

clean: ## Limpar containers e imagens
	docker-compose down -v --rmi all
	docker system prune -f

logs: ## Ver logs da aplicação
	docker-compose logs -f auth-service

test: ## Testar a API (health check)
	curl -X GET http://localhost:5000/health

shell: ## Acessar shell do container
	docker-compose exec auth-service /bin/bash