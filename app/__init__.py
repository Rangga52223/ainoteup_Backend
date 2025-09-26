from fastapi import FastAPI
from app.route.auth_route import authen
app = FastAPI(
    title="AINoteUp API",
    version="Alpha 1.0.0",
    description="App to managementyour life with AI",
)

# app.include_router(note)
# app.include_router(ai)
app.include_router(authen)