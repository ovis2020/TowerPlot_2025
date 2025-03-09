import os
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from google.cloud import storage, firestore

# ✅ Load Google Cloud credentials from environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "C:/Users/rfuen/Desktop/TowerPlot/gcs-key.json")

# ✅ Initialize Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "your_secure_secret_key")  # Secure secret key

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# ✅ Google Cloud Storage setup
BUCKET_NAME = "towerbucket1"
storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)

# ✅ Firestore setup for user authentication
db = firestore.Client()

# ✅ User Model (Stored in Firestore)
class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        """Save user to Firestore."""
        db.collection("users").document(self.username).set({
            "username": self.username,
            "password": self.password
        })

    @staticmethod
    def find_by_username(username):
        """Retrieve user from Firestore."""
        doc = db.collection("users").document(username).get()
        return User(doc.get("username"), doc.get("password")) if doc.exists else None

@login_manager.user_loader
def load_user(username):
    return User.find_by_username(username)

# ✅ Upload JSON to Google Cloud Storage
def upload_json_to_gcs(file_name, data):
    """Uploads JSON file to Google Cloud Storage."""
    blob = bucket.blob(file_name)
    blob.upload_from_string(json.dumps(data), content_type="application/json")
    return f"https://storage.googleapis.com/{BUCKET_NAME}/{file_name}"

# ✅ Download JSON from Google Cloud Storage
def download_json_from_gcs(file_name):
    """Downloads JSON file from Google Cloud Storage."""
    blob = bucket.blob(file_name)
    if blob.exists():
        return json.loads(blob.download_as_text())
    return None

# ✅ Home Page (Tower Input Form)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            tower_data = {
                "Tower Base Width": float(request.form["tower_base_width"]),
                "Top Width": float(request.form["top_width"]),
                "Height": float(request.form["height"]),
                "Variable Segments": int(request.form["variable_segments"]),
                "Constant Segments": int(request.form["constant_segments"]),
                "Total Segments": int(request.form["variable_segments"]) + int(request.form["constant_segments"]),
                "Cross Section": request.form["cross_section"],
                "Exposure Category": request.form["exposure_category"],
                "Importance Factor": float(request.form["importance_factor"]),
                "Basic Wind Speed Service": float(request.form["wind_speed_service"]),
                "Basic Wind Speed Ultimate": float(request.form["wind_speed_ultimate"]),
            }

            file_name = f"towers/tower_{tower_data['Height']}.json"
            file_url = upload_json_to_gcs(file_name, tower_data)

            return render_template("results.html", tower_data=tower_data, file_url=file_url)
        except ValueError:
            return jsonify({"error": "Invalid input. Please enter numerical values."})

    return render_template("index.html")

# ✅ Download Tower JSON
@app.route("/download_json/<tower_id>")
def download_json(tower_id):
    """Download tower JSON from GCS."""
    file_name = f"towers/tower_{tower_id}.json"
    tower_data = download_json_from_gcs(file_name)
    if tower_data:
        return jsonify(tower_data)
    return jsonify({"error": "Tower JSON not found"}), 404

# ✅ User Registration
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        if User.find_by_username(username):
            return jsonify({"error": "Username already exists"}), 400

        new_user = User(username, hashed_password)
        new_user.save_to_db()
        return redirect(url_for("login"))

    return render_template("register.html")

# ✅ User Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.find_by_username(username)

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("dashboard"))
        return jsonify({"error": "Invalid username or password"}), 401

    return render_template("login.html")

# ✅ User Dashboard (Requires Login)
@app.route("/dashboard")
@login_required
def dashboard():
    return f"Welcome, {current_user.username}! <a href='/logout'>Logout</a>"

# ✅ User Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

# ✅ Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
