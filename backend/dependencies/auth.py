from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth
from core.config import firebase_admin 


security = HTTPBearer()

def get_current_user(res: HTTPAuthorizationCredentials = Depends(security)):
    token = res.credentials
    try:

        decoded_token = auth.verify_id_token(token)
        
        user_id = decoded_token.get("uid")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token không chứa UID người dùng"
            )
            
        return user_id
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Xác thực thất bại: {str(e)}"
        )