# Variables for easy configuration
COMPOSE_FILE = docker-compose.yml
PROJECT_NAME = payouts_service
MANAGE = python manage.py

# Build and start services in detached mode
build:
	docker-compose -f ${COMPOSE_FILE} --project-name ${PROJECT_NAME} up --build -d

# Start already built services
up:
	docker-compose -f ${COMPOSE_FILE} --project-name ${PROJECT_NAME} up -d

# Stop all services
down:
	docker-compose -f ${COMPOSE_FILE} --project-name ${PROJECT_NAME} down

# Stop and remove all volumes (hard reset)
down-v:
	docker-compose -f ${COMPOSE_FILE} --project-name ${PROJECT_NAME} down -v

# Apply database migrations
migrate:
	docker-compose exec web ${MANAGE} migrate

# Create new migrations for the payout app
makemigrations:
	docker-compose exec web ${MANAGE} makemigrations payouts

# Run full test suite
test:
	docker-compose exec web ${MANAGE} test payouts

# Run specific test target (usage: make test-target TARGET=payouts.tests.test_api)
test-target:
	docker-compose exec web ${MANAGE} test $(TARGET) --keepdb

# Restart the Celery worker container
worker-restart:
	docker-compose restart celery_worker

# Follow logs for a specific service (usage: make logs SERVICE=web)
logs:
	docker-compose logs -f $(SERVICE)

# Open Django interactive shell
shell:
	docker-compose exec web ${MANAGE} shell
