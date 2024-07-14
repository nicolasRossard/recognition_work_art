run:
	cd backend/ && uvicorn app.main:app --reload --env-file ../.local_env

clean:
	docker compose down -v
	sudo rm -rf db/data/

run_db:
	docker compose up db