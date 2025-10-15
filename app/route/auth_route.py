from app.route import authen
from fastapi import Depends
from app.response.base_response import error_response
from app.helper.pydantict_helper import User, LoginRequest
from app.middleware.auth import register, login, logout
@authen.post('/register')
async def register_route(user:User):
    if user == None:
        return error_response(400, 'Tidak ada data yang masuk')
    print('Debug: masuk /register')
    print(f'Debug: isi user: {user}')
    return register(user)

@authen.post('/login')
async def login_route(request:LoginRequest):
    if request == None:
        return error_response(400, 'Tidak ada data yang masuk atau kosong')
    return login(request)

@authen.post('/logout')
async def logout_route(result = Depends(logout)):
    """
    Route untuk logout; menggunakan dependency logout dari middleware
    (token diambil otomatis dari Authorization header).
    """
    return result