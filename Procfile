web: gunicorn -w 1 -k uvicorn.workers.UvicornWorker main:app
worker: python app\services\telebot.py