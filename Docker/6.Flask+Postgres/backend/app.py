from flask import Flask, request, render_template_string
from flask_sqlalchemy import SQLAlchemy
import os
from time import sleep

app = Flask(__name__)

# Czekamy chwilę aż PostgreSQL się uruchomi
sleep(5)

# Konfiguracja bazy
db_user = os.getenv('POSTGRES_USER')
db_pass = os.getenv('POSTGRES_PASSWORD')
db_host = os.getenv('POSTGRES_HOST')
db_port = os.getenv('POSTGRES_PORT')
db_name = os.getenv('POSTGRES_DB')

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model danych — nasza tabela
class User(db.Model):
    __tablename__ = 'my_app_table'  # <<< NAZWA TABELI
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

# Tworzymy tabelę automatycznie przy starcie
with app.app_context():
    try:
        db.create_all()
        print("✅ Połączono z bazą i utworzono tabelę (jeśli nie istniała).")
    except Exception as e:
        print(f"❌ Błąd połączenia z bazą: {e}")

# Prosty HTML
html = """
<!DOCTYPE html>
<html>
  <body>
    <h2>Dodaj użytkownika</h2>
    <form method="POST" action="/">
      <input type="text" name="name" placeholder="Imię" required>
      <button type="submit">Zapisz</button>
    </form>
    <h3>Lista użytkowników:</h3>
    <ul>
      {% for user in users %}
        <li>{{ user.name }}</li>
      {% endfor %}
    </ul>
  </body>
</html>
"""

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
