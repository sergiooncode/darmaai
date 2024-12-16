COMPOSE_CMD = TAG=$(tag) docker compose

app_env = local
tag = latest

.PHONY: build
build: ## Build docker image including base dependencies
	$(COMPOSE_CMD) --progress plain build \
	$(service)

.PHONY: external-net
external-net: SERVICE_GRP_NET=service-grp-net
external-net: ## Create common external docker network (if missing).
	# this network is shared across services and marked as external in docker compose (thus not managed by it).
	@if [ "$$(docker network ls --filter name=$(SERVICE_GRP_NET) --format '{{ .Name }}')" != $(SERVICE_GRP_NET) ]; then \
       docker network create $(SERVICE_GRP_NET); \
    fi

.PHONY: up
up: # Boot up containers
	$(COMPOSE_CMD) up -d
	sleep 1
	$(COMPOSE_CMD) ps

.PHONY: migrate
migrate:
	$(COMPOSE_CMD) run --rm summarization-server sh -c "python manage.py migrate --database=default --noinput"

.PHONY: recreate
recreate: build external-net up migrate

.PHONY: down
down: # Stop containers
	$(COMPOSE_CMD) down

.PHONY: logs
logs:
	$(COMPOSE_CMD) logs -f

.PHONY: test
test:
	$(COMPOSE_CMD) run --rm summarization-server sh -c "pytest -sk /opt/darmaai/src/tests/"
