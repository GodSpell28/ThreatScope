.PHONY: install install-dev lint lint-backend lint-frontend test test-backend docker-up docker-down seed-mitre seed-es dev-backend dev-frontend

install:
	pip install -r backend/requirements.txt

install-dev:
	pip install -r backend/requirements.txt
	pip install pytest pytest-asyncio httpx ruff bandit

lint-backend:
	ruff check backend/

lint-frontend:
	cd frontend && npm install && npm run lint

lint: lint-backend lint-frontend

test-backend:
	cd backend && pytest ../tests -q

test: test-backend

docker-up:
	docker compose up --build

docker-down:
	docker compose down

seed-mitre:
	cd backend && python scripts/seed_mitre.py --reset

seed-es:
	cd backend && python scripts/seed_elasticsearch.py --reset

dev-backend:
	cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

dev-frontend:
	cd frontend && npm install && npm run dev
