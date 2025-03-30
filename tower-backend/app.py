import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from google.cloud import storage, firestore
from flask_cors import CORS
from dotenv import load_dotenv
from loadEngine.geometry import Geometry
from secction import Section  
from utils import normalizeTowerDataKeys


# ✅ Load environment variables
load_dotenv()

# ✅ Check if the path is loaded correctly
gcs_key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not gcs_key_path or not os.path.exists(gcs_key_path):
    raise FileNotFoundError(f"❌ Google Cloud credentials file not found: {gcs_key_path}")

print(f"✅ Using Google Cloud credentials from: {gcs_key_path}")

# ✅ Set Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = gcs_key_path

# ✅ Initialize Flask app
app = Flask(__name__, static_folder="../tower-frontend/dist", static_url_path="/")
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "default_secret_key")

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

CORS(app)  # ✅ Allow requests from React frontend

# ✅ Google Cloud Storage setup
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
BUCKET_NAME = os.getenv("BUCKET_NAME", "default-bucket-name")
storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)

# ✅ Firestore setup for user authentication
db = firestore.Client()

# ✅ User Model (Stored in Firestore)
class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_id(self):
        """Returns the username as Flask-Login requires a unique identifier."""
        return self.username

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
        if doc.exists:
            return User(doc.get("username"), doc.get("password"))
        return None

@login_manager.user_loader
def load_user(username):
    return User.find_by_username(username)

# ✅ Upload JSON to Google Cloud Storage
def upload_json_to_gcs(file_name, data):
    """Uploads JSON file to Google Cloud Storage."""
    try:
        blob = bucket.blob(file_name)
        blob.upload_from_string(json.dumps(data), content_type="application/json")
        return f"https://storage.googleapis.com/{BUCKET_NAME}/{file_name}"
    except Exception as e:
        print(f"❌ Error uploading JSON: {str(e)}")
        return None

# ✅ Download JSON from Google Cloud Storage
def download_json_from_gcs(file_name):
    """Downloads JSON file from Google Cloud Storage."""
    try:
        blob = bucket.blob(file_name)
        if not blob.exists():
            return None
        return json.loads(blob.download_as_text())
    except Exception as e:
        print(f"❌ Error downloading JSON: {str(e)}")
        return None

# ✅ Serve React Vite Frontend
@app.route("/")
def serve_react():
    """Serve React frontend from Vite build folder."""
    return send_from_directory(app.static_folder, "index.html")

# ✅ API Endpoint: Create a Tower (POST)
@app.route("/api/towers", methods=["POST"])
def create_tower():
    try:
        data = request.json
        tower_id = data.get("tower_id")
        if not tower_id:
            return jsonify({"error": "Tower ID is required"}), 400

        file_name = f"towers/tower_{tower_id}.json"
        file_url = upload_json_to_gcs(file_name, data)

        if not file_url:
            return jsonify({"error": "Failed to upload tower data"}), 500

        return jsonify({"message": "Tower created successfully", "url": file_url})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/towers", methods=["GET"])
def get_towers():
    """Fetch all stored towers."""
    try:
        blobs = bucket.list_blobs(prefix="towers/")
        towers = []
        for blob in blobs:
            tower_data = json.loads(blob.download_as_text())
            towers.append(tower_data)
        return jsonify(towers)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ API Endpoint: Fetch Tower Data (GET)
@app.route("/api/download_json/<tower_id>")
def download_json(tower_id):
    """Fetch tower JSON data."""
    file_name = f"towers/tower_{tower_id}.json"
    tower_data = download_json_from_gcs(file_name)

    if not tower_data:
        return jsonify({"error": "Tower not found"}), 404

    return jsonify(tower_data)

# ✅ API Endpoint: User Registration (POST)
@app.route("/api/register", methods=["POST"])
def register():
    try:
        data = request.json
        username = data["username"]
        password = data["password"]
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        if User.find_by_username(username):
            return jsonify({"error": "Username already exists"}), 400

        new_user = User(username, hashed_password)
        new_user.save_to_db()
        return jsonify({"message": "User registered successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ API Endpoint: User Login (POST)
@app.route("/api/login", methods=["POST"])
def login():
    try:
        data = request.json
        username = data["username"]
        password = data["password"]
        user = User.find_by_username(username)

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return jsonify({"message": "Login successful"})
        return jsonify({"error": "Invalid credentials"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ API Endpoint: User Logout (GET)
@app.route("/api/logout")
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"})


@app.route("/api/calculate/segments/<tower_id>", methods=["GET"])
def calculate_segments_from_json(tower_id):
    file_name = f"towers/tower_{tower_id}.json"
    tower_data = download_json_from_gcs(file_name)

    if not tower_data:
        return jsonify({"error": "Tower data not found"}), 404

    try:
        # Initialize Geometry with tower_data
        geometry = Geometry(
            tower_base_width=float(tower_data["Tower Base Width"]),
            top_width=float(tower_data["Top Width"]),
            height=float(tower_data["Height"]),
            variable_segments=int(tower_data["Variable Segments"]),
            constant_segments=int(tower_data["Constant Segments"]),
            cross_section=tower_data["Cross Section"]
        )

        segment_list = geometry.calculate_segments()

        return jsonify({
            "tower_id": tower_id,
            "segments": segment_list
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/api/calculate/section/<tower_id>", methods=["POST"])
def calculate_section_and_save(tower_id):
    try:
        tower_data = request.json
        towerData = normalizeTowerDataKeys(tower_data)

        section = Section(towerData)
        result = {
            "coordinates": section.getCoordinates(),
            "elements": section.getElements()
        }

        file_name = f"sections/tower_sections_{tower_id}.json"
        file_url = upload_json_to_gcs(file_name, result)

        return jsonify({
            "message": "Section data calculated and uploaded successfully",
            "tower_id": tower_id,
            "url": file_url,
            "data": result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/calculate/section-json", methods=["POST"])
def calculate_section_from_json():
    try:
        tower_data = request.json
        towerData = normalizeTowerDataKeys(tower_data)

        section = Section(towerData)

        return jsonify({
            "coordinates": section.getCoordinates(),
            "elements": section.getElements()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Run Flask App
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
