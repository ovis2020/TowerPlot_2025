import os
import json
from google.cloud import storage

# Explicitly set the credentials path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/rfuen/Desktop/TowerPlot/gcs-key.json"

# Initialize Google Cloud Storage
storage_client = storage.Client()
bucket_name = "towerbucket1"
bucket = storage_client.bucket(bucket_name)

def upload_json_to_gcs(file_name, data):
    """Uploads JSON file to Google Cloud Storage."""
    blob = bucket.blob(file_name)
    blob.upload_from_string(json.dumps(data), content_type="application/json")
    return f"https://storage.googleapis.com/{bucket_name}/{file_name}"

# Test JSON data
test_data = {
    "tower_id": "001",
    "height": 50,
    "location": "Chile",
    "antennas": ["Antenna 1", "Antenna 2"]
}

# File name in GCS
json_file_name = "test_tower.json"

# Upload JSON to GCS
file_url = upload_json_to_gcs(json_file_name, test_data)

print(f"✅ JSON file uploaded successfully! Access it here: {file_url}")

def download_json_from_gcs(file_name):
    """Downloads JSON file from Google Cloud Storage."""
    blob = bucket.blob(file_name)
    if blob.exists():
        json_data = blob.download_as_text()
        return json.loads(json_data)
    return None

# Retrieve JSON file
retrieved_data = download_json_from_gcs(json_file_name)

if retrieved_data:
    print("✅ JSON file downloaded successfully! Data:")
    print(json.dumps(retrieved_data, indent=4))
else:
    print("❌ JSON file not found in GCS.")