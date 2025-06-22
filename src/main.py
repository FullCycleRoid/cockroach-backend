from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from src.database import engine, SessionLocal, Base
from src import models
from src.endpoints import game, player, websocket
from src.websockets.manager import ws_manager

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Cockroach Game API",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(game.router, prefix="/api/games", tags=["games"])
app.include_router(player.router, prefix="/api/players", tags=["players"])
app.include_router(websocket.router, prefix="/ws", tags=["websocket"])

@app.on_event("startup")
async def startup_event():
    await ws_manager.connect_redis()
    print("Application started. Redis connected.")

@app.on_event("shutdown")
async def shutdown_event():
    await ws_manager.disconnect_redis()
    print("Application shutdown. Redis disconnected.")

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Cockroach Game API is running"}