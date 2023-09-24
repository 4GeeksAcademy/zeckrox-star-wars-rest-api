"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, People, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints

@app.route("/")# Aquí definimos el primer path de la API: GET /
def hello():
    return "Hello World!"  # Aquí flask devolverá "Hello World, esto podría ser un string HTML o un string JSON.

@app.route("/users", methods=["POST"])
def post_message():
    body = request.get_json()

    username = body.get("username", None)
    email = body.get("email", None)
    password = body.get("password", None)

    new_user = User( username=username, email=email, password=password )
    db.session.add(new_user)
    db.session.commit()
    return new_user.serialize(), 200

@app.route("/users", methods=["GET"])
def get_users():
    all_users = User.query.all()
    return [user.serialize() for user in all_users]

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user_id(user_id):
    try:
        selected_user = User.query.get(user_id) or None
        if selected_user == None:
            return "jaja error"
        else:
            return selected_user.serialize()
    
    except ValueError as err:
        return {"message": "failed to retrieve user " + err}, 500

@app.route("/users/<int:user_id>/favorites", methods=["GET"])
def get_favorites(user_id):
    try:
        user_favorites = Favorite.query.filter(Favorite.user_id == user_id)
        
        return [favorite.serialize() for favorite in user_favorites]
        
    except ValueError as err:
        return {"message": "failed to retrieve user " + err}, 500


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
