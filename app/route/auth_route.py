from app.route import authen
from fastapi import HTTPException
from app.helper.pydantict_helper import User, LoginRequest
from app.middleware.auth import register, login
@authen.post('/register')
async def register_route(user:User):
    if user == None:
        return HTTPException(status_code=400, detail='No Json Register')
    print('Debug: masuk /register')
    print(f'Debug: isi user: {user}')
    return register(user)

@authen.post('/login')
async def login_route(request:LoginRequest):
    if request == None:
        return HTTPException(status_code=400, detail='Request Not Found')
    return login(request)