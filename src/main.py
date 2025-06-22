from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from src.database import engine, SessionLocal
from src import models
from src.endpoints import game, player, websocket  # invite
from src.websockets.manager import ws_manager

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cockroach Game API")

# CORS настройки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(game.router, prefix="/api/games", tags=["games"])
app.include_router(player.router, prefix="/api/players", tags=["players"])
app.include_router(invite.router, prefix="/api/invites", tags=["invites"])
app.include_router(websocket.router, prefix="/ws", tags=["websocket"])

@app.on_event("startup")
async def startup_event():
    await ws_manager.connect_redis()

@app.on_event("shutdown")
async def shutdown_event():
    await ws_manager.disconnect_redis()