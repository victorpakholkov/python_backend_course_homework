import uvicorn as uvicorn
from fastapi import FastAPI
from config.celery_utils import create_celery
from routers import universities


def create_app() -> FastAPI:
    current_app = FastAPI(title="HW4 - Celery and RabbitMQ")

    current_app.celery_app = create_celery()
    current_app.include_router(universities.router)
    return current_app


app = create_app()
celery = app.celery_app


if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, reload=True)


# python main.py
# celery -A main.celery worker --loglevel=info -Q universities,university
# celery -A main.celery flower --port=5555
