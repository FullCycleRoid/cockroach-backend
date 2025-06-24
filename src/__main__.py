from contextlib import asynccontextmanager

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from endpoints import game, player, websocket
from sockets.manager import ws_manager
from src.config import settings

Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await ws_manager.connect_redis()
    print("✅ Application started. Redis connected.")

    yield

    await ws_manager.disconnect_redis()
    print("🔌 Application shutdown. Redis disconnected.")


app = FastAPI(
    title="Cockroach Game API",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
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

from fastapi.websockets import WebSocket


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"You said: {data}")


@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        # Проверка подключения к PostgreSQL
        db.execute("SELECT 1")
        db_ok = True
    except Exception:
        db_ok = False

    try:
        # Проверка подключения к Redis
        await ws_manager.redis.ping()
        redis_ok = True
    except Exception:
        redis_ok = False

    status = "ok" if db_ok and redis_ok else "degraded"

    return {
        "status": status,
        "database": "ok" if db_ok else "unavailable",
        "redis": "ok" if redis_ok else "unavailable",
    }


if __name__ == "__main__":
    if settings.ENVIRONMENT.is_local:
        uvicorn.run(
            "src.__main__:app", host="0.0.0.0", port=8000, reload=True, workers=1
        )
