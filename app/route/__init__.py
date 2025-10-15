from fastapi import APIRouter

note = APIRouter(
    prefix="/api/v1/note",
    tags=["notepad"]
)

# ai = APIRouter(
#     prefix="/api/v1/ask",
#     tags=["ask_AI"]
# )

authen = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentikasi"]
)