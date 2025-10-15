from fastapi import FastAPI
from app.route.auth_route import authen
from app.route.note_route import note
# from app.route.ai_route import ai
app = FastAPI(
    title="AINoteUp API",
    version="Alpha 1.0.0",
    description="App to management your life with AI",
    openapi_url=None,      
    docs_url=None,         
    redoc_url=None         
)

app.include_router(note)
# app.include_router(ai)
app.include_router(authen)