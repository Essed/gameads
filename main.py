from fastapi import FastAPI
import uvicorn
from fastapi.routing import APIRouter
from api.user_handlers import user_router
from api.login_handler import login_router
from api.adcamping_handler import campaing_router
from api.game_handler import game_router
from api.upload_handler import upload_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="GameAds")
app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)

main_api_router = APIRouter()

main_api_router.include_router(user_router, prefix="/user", tags=['user'])
main_api_router.include_router(login_router, prefix="/login", tags=['login'])
main_api_router.include_router(campaing_router, prefix="/campaigns", tags=['campaigns'])
main_api_router.include_router(game_router, prefix="/games", tags=['games'])
main_api_router.include_router(upload_router, prefix="/img", tags=['img'])
app.include_router(main_api_router)
app.mount("/img", StaticFiles(directory="img"), "img")


if __name__ == "__main__":
    uvicorn.run(app, host="26.3.189.182", port=8000)