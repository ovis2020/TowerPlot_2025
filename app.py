from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import json
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# ✅ User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ✅ Route: Home Page (Tower Input Form)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            tower_base_width = float(request.form["tower_base_width"])
            top_width = float(request.form["top_width"])
            height = float(request.form["height"])
            variable_segments = int(request.form["variable_segments"])
            constant_segments = int(request.form["constant_segments"])
            cross_section = request.form["cross_section"]
            exposure_category = request.form["exposure_category"]
            importance_factor = float(request.form["importance_factor"])
            wind_speed_service = float(request.form["wind_speed_service"])
            wind_speed_ultimate = float(request.form["wind_speed_ultimate"])

            # ✅ Create JSON Data
            tower_data = {
                "Tower Base Width": tower_base_width,
                "Top Width": top_width,
                "Height": height,
                "Variable Segments": variable_segments,
                "Constant Segments": constant_segments,
                "Total Segments": variable_segments + constant_segments,
                "Cross Section": cross_section,
                "Exposure Category": exposure_category,
                "Importance Factor": importance_factor,
                "Basic Wind Speed Service": wind_speed_service,
                "Basic Wind Speed Ultimate": wind_speed_ultimate,
            }

            json_filename = "tower_data.json"
            with open(json_filename, "w") as f:
                json.dump(tower_data, f, indent=4)

            return render_template("results.html", tower_data=tower_data, json_filename=json_filename)

        except ValueError:
            return jsonify({"error": "Invalid input. Please enter numerical values."})

    return render_template("index.html")

# ✅ Route: Download JSON File
@app.route("/download_json/<filename>")
def download_json(filename):
    return f"Download JSON: <a href='/{filename}'>{filename}</a>"

# ✅ Route: User Registration
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))

    return render_template("register.html")

# ✅ Route: User Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("dashboard"))

    return render_template("login.html")

# ✅ Route: User Dashboard (Requires Login)
@app.route("/dashboard")
@login_required
def dashboard():
    return f"Welcome, {current_user.username}! <a href='/logout'>Logout</a>"

# ✅ Route: User Logout
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

# ✅ Ensure Database Tables Are Created
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
