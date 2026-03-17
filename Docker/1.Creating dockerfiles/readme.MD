# Flask App in Docker

This is a simple Python Flask application running inside Docker.

## Files

- `Dockerfile` – defines the container image
- `app.py` – simple Flask API with in-memory data
- `requirements.txt` – dependencies


## How to run

1. Build the image:
   ```bash
   docker build -t flask-app .
   ```

2. Run the container:
   ```bash
   docker run -p 8080:5000 flask-app
   ```

3. Open in browser:
   - [http://localhost:8080](http://localhost:8080)
   - [http://localhost:8080/items](http://localhost:8080/items)

