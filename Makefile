copy_env_files:
	cp ./envs/app.env.example ./envs/app.env
	cp ./envs/db.env.example ./envs/db.env
	cp ./env.example ./.env

run:
	docker compose build --no-cache
	make migrate
	make create_superuser
	docker compose up --remove-orphans --force-recreate

run_detach:
	docker compose build --no-cache
	make migrate
	make create_superuser
	docker compose up --remove-orphans --force-recreate --detach

backend_build:
	docker compose build backend-dev --no-cache

migrate:
	docker compose run --rm backend-dev sh -c "python manage.py makemigrations"
	docker compose run --rm backend-dev sh -c "python manage.py migrate"

create_superuser:
	docker compose run --rm backend-dev sh -c "python manage.py create_superuser"

backend_up:
	docker compose up backend-dev --remove-orphans --force-recreate

backend_up_detach:
	docker compose up backend-dev --remove-orphans --force-recreate --detach

db_build_up:
	docker compose build db --no-cache
	docker compose up db --remove-orphans --force-recreate

db_build_up_detach:
	docker compose build db --no-cache
	docker compose up db --remove-orphans --force-recreate --detach

adminer_build_up:
	docker compose build adminer --no-cache
	docker compose up adminer --remove-orphans --force-recreate

adminer_build_up_detach:
	docker compose build adminer --no-cache
	docker compose up adminer --remove-orphans --force-recreate --detach

down:
	docker compose down

tests:
	docker compose run --rm backend-dev sh -c "python manage.py test --verbosity=$(v) $(target)"

tests_all:
	docker compose run --rm backend-dev sh -c "python manage.py test --verbosity=$(v) ."

# Help target
.PHONY: help

help:
	@echo "Available Commands:"
	@echo "  copy_env_files          - Copy environment example files to actual environment files."
	@echo "  run                     - Build and run the application with a fresh setup."
	@echo "  run_detach              - Build and run the application in detached mode with a fresh setup."
	@echo "  backend_build           - Build the backend container without cache."
	@echo "  migrate                 - Run Django migrations."
	@echo "  create_superuser        - Create a Django superuser, using credentials in app.env file."
	@echo "  backend_up              - Start the backend container."
	@echo "  backend_up_detach       - Start the backend container in detached mode."
	@echo "  db_build_up             - Build and start the database container."
	@echo "  db_build_up_detach      - Build and start the database container in detached mode."
	@echo "  adminer_build_up        - Build and start the Adminer container."
	@echo "  adminer_build_up_detach - Build and start the Adminer container in detached mode."
	@echo "  down                    - Stop and remove all Docker containers."
	@echo "  tests                   - Run tests with specified verbosity and target."
	@echo "  tests_all               - Run all tests with specified verbosity."

	@echo ""
	@echo "Example Usage:"
	@echo "  make copy_env_files"
	@echo "  make run"
	@echo "  make run_detach"
	@echo "  make backend_build"
	@echo "  make migrate"
	@echo "  make create_superuser"
	@echo "  make backend_up"
	@echo "  make backend_up_detach"
	@echo "  make db_build_up"
	@echo "  make db_build_up_detach"
	@echo "  make adminer_build_up"
	@echo "  make adminer_build_up_detach"
	@echo "  make down"
	@echo "  make tests v=2 target=apps.tests.purchases"
	@echo "  make tests_all v=2"

