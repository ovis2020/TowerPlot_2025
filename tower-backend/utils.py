from google.cloud import storage
import json
import os

def normalizeTowerDataKeys(data):
    return {
        "tower_base_width": float(data.get("Tower Base Width") or data.get("tower_base_width")),
        "top_width": float(data.get("Top Width") or data.get("top_width")),
        "height": float(data.get("Height") or data.get("height")),
        "variable_segments": int(data.get("Variable Segments") or data.get("variable_segments")),
        "constant_segments": int(data.get("Constant Segments") or data.get("constant_segments")),
        "cross_section": (data.get("Cross Section") or data.get("cross_section") or "square").lower()
    }



def download_json_from_gcs(file_path):
    print(f"📁 GCS Download Request: {file_path}")
    
    bucket_name = os.getenv("BUCKET_NAME") or "towerbucket1"
    print(f"🪣 Bucket: {bucket_name}")
    
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_path)

    # ✅ Optional: check if file exists before download
    if not blob.exists():
        raise FileNotFoundError(f"❌ File '{file_path}' not found in bucket '{bucket_name}'")

    content = blob.download_as_text()
    print("📄 GCS Raw Content (first 200 chars):", content[:200])
    return json.loads(content)
