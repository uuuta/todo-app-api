from fastapi import Request, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import ValidationError

from schemas.user import User

security = HTTPBearer()


def get_authorized_user(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    # システム要件に応じて、認証処理やJWTのデコード等 ここでは代入のみ
    user_id = credentials.credentials
    try:
        return User(id=user_id)
    except ValidationError:
        raise HTTPException(status_code=403, detail="Invalid user")
