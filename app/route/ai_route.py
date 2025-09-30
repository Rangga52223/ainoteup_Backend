from app.route import ai
from app.helper.pydantict_helper import Ask
from fastapi import HTTPException, Depends
from app.middleware.auth import session_checking
from app.service.chat_service import Asked_AI
@ai.post('')
def ai_ask_route(ask:Ask, user: str = Depends(session_checking)):
    try:
        if ask == None:
            return HTTPException(400, 'No Question Input')
        return Asked_AI(ask, user)
    except Exception as e:
        print(f'Debug_Error:{str(e)}')
        return HTTPException(status_code=400, detail=f'Error di ai_ask_route:{str(e)}')
