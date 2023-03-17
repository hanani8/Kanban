KANBANV2 - Hanani Bathina, 21F1006169

A.) For starting up the Flask application: 
1. Ensure you are in the backend directory (cd backend). 
2. Run the app.py file (python3 main.py).

B.) For starting the VueJS system: 
1. Ensure you are in the frontend directory (cd frontend)
2. Run the command npm run serve
3. For the PWA version, use the following commands in the terminal -  npm run build;npx http-server dist

C.) For starting the Redis server: 
1. Run the command redis-server

D.) For starting the Celery beat
1. Navigate to backend directory (cd backend)
2. Run the command celery -A main.celery beat

E.) For starting Celery worker:
1. Navigate to the backend directory (cd backend)
2. Run the command celery -A main.celery worker --loglevel=info


(Each of the 5 features/tasks has to be performed in separate, concurrently running terminals in Linux/WSL)
