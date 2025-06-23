from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base, get_db
from sqlalchemy.orm import Session
from endpoints import game, player, websocket
from websockets.manager import ws_manager

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
    print("✅ Application started. Redis connected.")

@app.on_event("shutdown")
async def shutdown_event():
    await ws_manager.disconnect_redis()
    print("🔌 Application shutdown. Redis disconnected.")

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
        "redis": "ok" if redis_ok else "unavailable"
    }
