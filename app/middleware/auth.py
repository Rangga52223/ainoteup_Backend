from fastapi import Depends, HTTPException
from app.database.database import SessionLocal
from app.model_db.user_id import User
from app.response.base_response import error_response, succes_response, auth_response
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta
from config import Config
import uuid
db = SessionLocal()

# --- ADDED: password context ---
# gunakan bcrypt_sha256 supaya panjang password >72 bytes ditangani (pre-hash dengan sha256)
pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return encoded_jwt

def register(user):
    try:
        existing = db.query(User).filter(User.user_name == user.username).first()
        if existing:
            raise HTTPException(status_code=400, detail="Username already exists")

        # hash password sebelum disimpan
        try:
            hashed_password = pwd_context.hash(user.password)
        except Exception as e:
            print(f"Password hashing error: {e}")
            return error_response(http_status=500, message="Password hashing failed")

        # buat instance dari model User (SQLAlchemy)
        new_user = User(
            user_id=uuid.uuid4(),
            user_name=user.username,
            password=hashed_password,
            tanggal_lahir=user.tanggal_lahir,
            pekerjaan=user.pekerjaan,
            jam_tidur=user.jam_tidur,
            jam_kerja=user.jam_kerja,
            punya_keluarga=user.punya_keluarga,
            agama=user.agama
        )

        # simpan ke DB
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return succes_response(http_status=200, message='User registered successfully')
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        db.rollback()  # Rollback on error
        print(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    

def login(request):
    user = db.query(User).filter(User.user_name == request.username).first()
    if not user:
        return error_response(http_status=401, message="Invalid username or password")

    # verifikasi password hash
    try:
        if not pwd_context.verify(request.password, user.password):
            return error_response(http_status=401, message="Invalid username or password")
    except Exception as e:
        print(f"Password verify error: {e}")
        return error_response(http_status=500, message="Password verify failed")

    # Token hanya simpan user_id + exp
    access_token = create_access_token(
        data={"user_id": str(user.user_id)}  # <-- user_id masuk payload
    )

    return auth_response(200, 'login sukses', user.user_id, access_token)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# --- moved/added: global revoked token store ---
_revoked_tokens: set[str] = set()

def session_checking(token: str = Depends(oauth2_scheme)):
    """
    Dependency untuk validasi JWT dari header Authorization Bearer
    """
    token_str = token  # oauth2_scheme sudah memberikan token tanpa "Bearer "
    # cek apakah token sudah di-revoke (logout)
    if token_str in _revoked_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")

    try:
        payload = jwt.decode(token_str, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        user_id: str = payload.get("user_id")
        exp = payload.get("exp")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        if exp and datetime.utcnow().timestamp() > exp:
            raise HTTPException(status_code=401, detail="Token expired")

        return str(user_id)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def logout(token: str = Depends(oauth2_scheme)):
    """
    Mark the provided access token as revoked so further requests using it are rejected.
    Note: this is an in-memory revocation. For persistence across restarts use DB or Redis.
    """
    try:
        # validasi token terlebih dahulu
        jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    _revoked_tokens.add(token)
    return succes_response(http_status=200, message="Logout successful")