# Payout Management Service

RESTful API for payout requests management with asynchronous Celery processing.

## 1. Quick Start (Docker)

The project is containerized. Commands to start:

- Build and run: docker-compose up --build -d
- Migrations: docker-compose exec web python manage.py migrate
- Tests: docker-compose exec web python manage.py test payouts

API URL:
http://localhost:8000/api/payouts/

Swagger:
http://localhost:8000/swagger/

---

## 2. Implementation Details

- Financial Precision: DecimalField for monetary operations with explicit validation in the serializer.
- System Reliability: Task dispatching via transaction.on_commit to ensure task is sent only after DB commit.
- Security: UUIDField for payout IDs to prevent enumeration.
- Validation: Strict checks for currency (ISO 4217) and positive amounts.

---

## 3. Production Deployment Info

### Infrastructure
- Web server: Nginx as a reverse proxy.
- App server: Gunicorn for Django and Celery worker.
- Database: Managed PostgreSQL.
- Broker: Redis with persistence.

### Deployment Strategy
1. Containerization: Docker images built via CI/CD.
2. Orchestration: Kubernetes or Docker Swarm for independent scaling of web and worker nodes.
3. Security: DEBUG=False, secrets managed via environment variables. Zero-downtime deployment with automated migrations.