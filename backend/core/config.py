import firebase_admin
from firebase_admin import credentials, firestore
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEY_PATH = os.path.join(BASE_DIR, "..", "serviceAccountKey.json")

def initialize_firebase():

    try:
        if not firebase_admin._apps:
            if not os.path.exists(KEY_PATH):
                print(f"LỖI: Không tìm thấy file {KEY_PATH}")
                return None
            
            cred = credentials.Certificate(KEY_PATH)
            firebase_admin.initialize_app(cred)
            print("--- Firebase Admin đã được khởi tạo thành công! ---")
            
        return firestore.client()
    except Exception as e:
        print(f"Lỗi khởi tạo Firebase: {e}")
        return None

db = initialize_firebase()