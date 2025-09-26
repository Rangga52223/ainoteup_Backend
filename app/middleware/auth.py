from fastapi import Depends, HTTPException
from app.database.database import SessionLocal
from app.model_db.user_id import User
from passlib.context import CryptContext
db = SessionLocal()



def register(user):
    try:
        existing = db.query(User).filter(User.user_name == user.username).first()
        if existing:
            raise HTTPException(status_code=400, detail="Username already exists")

        # buat instance dari model User (SQLAlchemy)
        new_user = User(
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

