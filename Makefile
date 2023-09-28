# Variáveis
DOCKER_COMPOSE = docker compose
SERVICE_NAMES = petwatch-api-backend petwatch-ai-engine petwatch-face-ui mysql minio
DB_URI = 'mysql://user:password@mysql/petwatch-ai-inference'

# Comandos
build:
	$(DOCKER_COMPOSE) build

run:
	$(DOCKER_COMPOSE) up -d

purge:
	$(DOCKER_COMPOSE) down --remove-orphans
	$(DOCKER_COMPOSE) rm -f

start:
	$(DOCKER_COMPOSE) start

logs:
	$(DOCKER_COMPOSE) logs -f $(SERVICE_NAMES)

mysql-shell:
	docker exec -it petwatch-mysql mysql -u user -p

init-db:
	docker exec -it petwatch-api-backend python -c "from app import create_db; create_db('$(DB_URI)')"

# Ajuda
help:
	@echo "Makefile para gerenciar serviços Docker para o Petwatch Monitoring System"
	@echo ""
	@echo "Comandos disponíveis:"
	@echo "  make build        - Build dos serviços"
	@echo "  make run          - Inicia os serviços em segundo plano"
	@echo "  make purge        - Remove todos os contêineres e volumes relacionados aos serviços"
	@echo "  make start        - Inicia os serviços (após uma execução anterior de make run ou make start)"
	@echo "  make logs         - Exibe os logs dos serviços"
	@echo "  make mysql-shell  - Acessa o shell do MySQL no contêiner do MySQL"
	@echo "  make init-db      - Inicializa o banco de dados (cria tabelas, insere dados iniciais, etc.)"
	@echo ""

# Regras
.PHONY: build run purge start logs mysql-shell init-db help
