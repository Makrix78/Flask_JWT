from flask import Flask, render_template, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_jwt_extended import JWTManager
from datetime import timedelta

app = Flask(__name__)

# Configuration du module JWT
app.config["JWT_SECRET_KEY"] = "Ma_clé_secrete"  # Ma clé privée
jwt = JWTManager(app)

# Exemple de base de données fictive pour les utilisateurs et leurs rôles
users_db = {
    "test": {"password": "test", "role": "user"},
    "admin": {"password": "admin", "role": "admin"}
}

@app.route('/images')
def images():
    return render_template('Correction_Images.html')

@app.route('/')
def hello_world():
    return render_template('accueil.html')

# Création d'une route qui vérifie l'utilisateur et retourne un jeton JWT
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    
    # Vérifiez si l'utilisateur existe dans la "base de données"
    user = users_db.get(username)
    
    if not user or user["password"] != password:
        return jsonify({"msg": "Mauvais utilisateur ou mot de passe"}), 401
    
    # Création du jeton avec un rôle inclus dans le payload
    expires = timedelta(hours=1)  # Le jeton expire dans 1 heure
    access_token = create_access_token(
        identity=username, 
        expires_delta=expires, 
        additional_claims={"role": user["role"]}  # Ajout du rôle à l'intérieur du jeton
    )
    return jsonify(access_token=access_token)

# Route protégée qui nécessite un rôle particulier
@app.route("/admin", methods=["GET"])
@jwt_required()
def admin():
    # Récupérer le rôle de l'utilisateur à partir du jeton
    current_user = get_jwt_identity()
    claims = get_jwt()["role"]  # Accéder aux données de rôle dans le jeton
    
    if claims != "admin":
        return jsonify({"msg": "Accès refusé. Vous devez être un admin."}), 403

    return jsonify(logged_in_as=current_user, msg="Bienvenue sur la page admin."), 200

# Route protégée générique pour les utilisateurs
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == "__main__":
    app.run(debug=True)
