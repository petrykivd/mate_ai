app:
	uvicorn src.main:app --port 8000 --reload

storage:
	cd docker && docker compose up

storage-down:
	cd docker && docker compose down
