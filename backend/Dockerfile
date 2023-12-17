FROM python:3.10.12

RUN mkdir ./app

WORKDIR /app/

RUN mkdir ./backend
RUN mkdir ./data

COPY . ./backend

RUN pip install -r ./backend/requirements.txt

CMD gunicorn backend.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000