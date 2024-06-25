clean_qdrant:
	docker compose down -v
	sudo rm -rf qdrant_storage

run_qdrant:
	docker compose up qdrant