# KANBAN

**Author**: Hanani Bathina
**Student ID**: 21F1006169

KANBANV2 is a project designed to replicate a Kanban board system. It utilizes a modern technology stack, including Vue 2 for the frontend, Flask for the backend, Celery for asynchronous job processing, and Redis for caching. Additionally, Flask-Security is used to enhance the security of the application.

## Getting Started

Follow these steps to set up and run KANBANV2 on your local machine:

### A. Starting the Flask Application

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Run the Flask application:
   ```bash
   python3 main.py
   ```

### B. Starting the VueJS System

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Start the VueJS development server:
   ```bash
   npm run serve
   ```

3. For the Progressive Web App (PWA) version, use the following commands in the terminal:
   ```bash
   npm run build
   npx http-server dist
   ```

### C. Starting the Redis Server

1. Start the Redis server:
   ```bash
   redis-server
   ```

### D. Starting Celery Beat

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Start Celery Beat for task scheduling:
   ```bash
   celery -A main.celery beat
   ```

### E. Starting Celery Worker

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Start Celery Worker for processing tasks with logging enabled:
   ```bash
   celery -A main.celery worker --loglevel=info
   ```

Ensure that each of the above steps is performed in separate, concurrently running terminals in Linux/WSL for proper system functionality.

## Technology Stack

- **Frontend**: Vue 2
- **Backend**: Flask
- **Asynchronous Processing**: Celery
- **Caching**: Redis
- **Security**: Flask-Security

If you have any questions, encounter issues, or would like to contribute to the project, please visit the [GitHub repository](https://github.com/hanani8/KANBANV2).

Happy Kanbaning!
