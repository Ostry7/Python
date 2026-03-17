# Flask + PostgreSQL with Docker Compose

## Overview
This project demonstrates a simple **MERN stack** setup using Docker Compose, which includes:

- **Flask (Python)** – web backend
- **PostgreSQL** – relational database
- **pgAdmin4** - graphical DB management tool
- **Docker Compose** container orchestration

---
## Environment setup

Create a `.env` file in the root directory:

```bash
POSTGRES_DB=flask_db
POSTGRES_USER=flask_user
POSTGRES_PASSWORD=flask_pass
POSTGRES_HOST=postgresql
POSTGRES_PORT=5432
```
or use
```bash
EXPORT $variable_name=value
```

---

## Example Flask App (backend/app.py)

```python
from flask import Flask, request, render_template_string
from flask_sqlalchemy import SQLAlchemy
import os
from time import sleep

app = Flask(__name__)

sleep(5)

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

with app.app_context():
    db.create_all()

html = '''
<!DOCTYPE html>
<html>
  <body>
    <h2>Add User</h2>
    <form method="POST" action="/">
      <input type="text" name="name" placeholder="Name" required>
      <button type="submit">Save</button>
    </form>
    <h3>Users:</h3>
    <ul>
      {% for user in users %}
        <li>{{ user.name }}</li>
      {% endfor %}
    </ul>
  </body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        if name:
            new_user = User(name=name)
            db.session.add(new_user)
            db.session.commit()
    users = User.query.all()
    return render_template_string(html, users=users)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

```

---

## Usage


### 1. Build and start the containers:

```bash
docker compose up --build -d
```

### 2. Access the services:

- Access the app at http://localhost:5000
- Access pgAdmin4 at http://localhost:8080

---

## Notes

- Flask connects to PostgreSQL using environment variables defined in .env.
- PostgreSQL persists data using the pgdata volume.
- pgAdmin4 is configured to connect to the PostgreSQL service.
- When the Flask container starts, it automatically creates tables via SQLAlchemy.

---

## Stop & Cleanup

```bash
docker compose down -v
```

---
