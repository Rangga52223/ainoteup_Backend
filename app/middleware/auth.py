from fastapi import Depends, HTTPException, status
from app.database.database import SessionLocal
from app.model_db.user_id import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta
import uuid
db = SessionLocal()

SECRET_KEY = "secretjwt123"   # ganti dengan yang aman
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def register(user):
    try:
        existing = db.query(User).filter(User.user_name == user.username).first()
        if existing:
            raise HTTPException(status_code=400, detail="Username already exists")

        # buat instance dari model User (SQLAlchemy)
        new_user = User(
            user_id=uuid.uuid4(),
            user_name=user.username,
            password=user.password,
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

        return {"message": "User registered successfully", "user_id": str(new_user.user_id)}
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        db.rollback()  # Rollback on error
        print(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    

def login(request):
    user = db.query(User).filter(User.user_name == request.username).first()
    if request.password != user.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Token hanya simpan user_id + exp
    access_token = create_access_token(
        data={"user_id": str(user.user_id)}  # <-- user_id masuk payload
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.user_id
    }

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
def session_checking(token: str = Depends(oauth2_scheme)):
    """
    Dependency untuk validasi JWT dari header Authorization Bearer
    """
    try:
        token_str = token or oauth2_scheme()  # ambil token dari header
        payload = jwt.decode(token_str, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        exp = payload.get("exp")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        if exp and datetime.utcnow().timestamp() > exp:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired"
            )

        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )