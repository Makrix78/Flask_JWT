from flask import Flask, render_template, jsonify, request, make_response
from flask_jwt_extended import (
    create_access_token, get_jwt_identity, jwt_required, JWTManager, get_jwt
)
from datetime import timedelta

app = Flask(__name__)

# Configuration du module JWT
app.config["JWT_SECRET_KEY"] = "Ma_clé_secrete"
jwt = JWTManager(app)

@app.route('/images')
def images():
    return render_template('Correction_Images.html')

@app.route('/')
def hello_world():
    return render_template('accueil.html')

@app.route('/formulaire')
def formulaire():
    return render_template('formulaire.html')

# Création d'un dictionnaire des utilisateurs avec rôles
users = {
    "test": {"password": "test", "role": "user"},
    "admin": {"password": "admin", "role": "admin"}
}

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = users.get(username, None)
    
    if not user or user["password"] != password:
        return jsonify({"msg": "Mauvais utilisateur ou mot de passe"}), 401
    
    expires = timedelta(hours=1)
    access_token = create_access_token(identity=username, expires_delta=expires, additional_claims={"role": user["role"]})
    
    response = make_response(jsonify({"msg": "Connexion réussie"}))
    response.set_cookie("access_token", access_token, httponly=True)
    return response

# Route protégée par un jeton valide
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# Route réservée aux administrateurs
@app.route("/admin", methods=["GET"])
@jwt_required()
def admin():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"msg": "Accès refusé : privilèges insuffisants"}), 403
    return jsonify({"msg": "Bienvenue, administrateur !"})

if __name__ == "__main__":
    app.run(debug=True)
