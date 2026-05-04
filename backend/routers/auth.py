from fastapi import APIRouter, Depends
from dependencies.auth import get_current_user
from fastapi.responses import RedirectResponse
import requests
import os
from dotenv import load_dotenv

load_dotenv(override=True)

router = APIRouter(prefix="/auth", tags=["Auth"])

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/auth/google/callback")
FIREBASE_WEB_API_KEY = os.getenv("FIREBASE_WEB_API_KEY", "")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8501")

@router.get("/google/start")
def google_login():
    if not GOOGLE_CLIENT_ID:
        return {"error": "Chưa cấu hình GOOGLE_CLIENT_ID"}
        
    url = f"https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20email%20profile&access_type=offline"
    return RedirectResponse(url)

@router.get("/google/callback")
def google_callback(code: str):
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    token_res = requests.post(token_url, data=data)
    token_json = token_res.json()
    
    if "id_token" not in token_json:
        return {"error": "Lỗi xác thực từ Google", "details": token_json}
        
    google_id_token = token_json["id_token"]
    
    
    firebase_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithIdp?key={FIREBASE_WEB_API_KEY}"
    payload = {
        "postBody": f"id_token={google_id_token}&providerId=google.com",
        "requestUri": "http://localhost:8000",
        "returnIdpCredential": True,
        "returnSecureToken": True
    }
    fb_res = requests.post(firebase_url, json=payload)
    fb_json = fb_res.json()
    
    if "idToken" not in fb_json:
        return {"error": "Lỗi xác thực Firebase", "details": fb_json}
        
    firebase_token = fb_json["idToken"]
    
    return RedirectResponse(f"{FRONTEND_URL}/?token={firebase_token}")

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth

security = HTTPBearer()

@router.get("/me")
def get_user_info(res: HTTPAuthorizationCredentials = Depends(security)):
    try:
        decoded_token = auth.verify_id_token(res.credentials)
        return {
            "status": "success",
            "user_id": decoded_token.get("uid"),
            "email": decoded_token.get("email", ""),
            "name": decoded_token.get("name", "Người dùng")
        }
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail=str(e))
