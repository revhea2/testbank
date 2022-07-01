from flask import Flask, render_template, send_from_directory
import dotenv
import os

from backend import db, ma, bcrypt, login_manager
from flask_migrate import Migrate
from flask_reggie import Reggie

app = Flask(__name__)

# Configuring the application from .env file
dotenv_path = os.path.join(os.getcwd(), '.env')
dotenv.load_dotenv(dotenv_path)

DB_URI = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

db.init_app(app)
migrate = Migrate(app, db)

# Regex converter
Reggie(app)

# Initializing marshmallow
ma.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)

# Make folder for temp question pdf folder
if not os.path.exists('./temp'):
    os.makedirs('./temp')


# # Register blueprints
# app.register_blueprint(api, url_prefix='/api/v1')

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    return render_template("index.html")


@app.route(r"/<regex('([a-zA-Z\_]+\/)*[a-zA-Z]+\.[a-zA-Z]+'):file>")
def serve_static(file):
    print(f"Looking for {file}")
    return send_from_directory(app.template_folder, file)


if __name__ == '__main__':
    app.run()
