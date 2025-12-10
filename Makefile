.PHONY: help install install-dev lint format run build docker-build docker-run

DOCKER_IMAGE_NAME := test-task-3d
DOCKER_TAG := latest

help:
	@echo "Available commands:"
	@echo "  make install       - Install production dependencies"
	@echo "  make install-dev   - Install development dependencies"
	@echo "  make lint          - Run ruff linter"
	@echo "  make format        - Format code with ruff"
	@echo "  make run           - Run the main script"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-run    - Run Docker container"

install:
	uv sync --no-dev

install-dev:
	uv sync

lint:
	uv run ruff check .

format:
	uv run ruff format .

run-local:
	uv run python distance_calculator.py

docker-build:
	DOCKER_SCAN_SUGGEST=false docker build -t $(DOCKER_IMAGE_NAME):$(DOCKER_TAG) -f Dockerfile .

docker-run:
	docker run --rm -it $(DOCKER_IMAGE_NAME):$(DOCKER_TAG)
