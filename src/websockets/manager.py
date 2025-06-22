import asyncio
import json
import redis.asyncio as redis
from collections import defaultdict

from starlette.websockets import WebSocket


class WebSocketManager:
    def __init__(self):
        self.active_connections = defaultdict(list)
        self.redis = None
        self.pubsub = None

    async def connect_redis(self):
        from src.database import settings
        self.redis = redis.Redis.from_url(settings.redis_url)
        self.pubsub = self.redis.pubsub()
        asyncio.create_task(self.listen_redis())

    async def disconnect_redis(self):
        if self.pubsub:
            await self.pubsub.close()
        if self.redis:
            await self.redis.close()

    async def listen_redis(self):
        await self.pubsub.psubscribe("game_updates:*")
        async for message in self.pubsub.listen():
            if message["type"] == "pmessage":
                channel = message["channel"].decode()
                game_id = channel.split(":")[1]
                data = message["data"]

                # Отправляем обновление всем подключенным клиентам
                for connection in self.active_connections.get(game_id, []):
                    await connection.send_text(data)

    async def connect(self, websocket: WebSocket, game_id: str):
        await websocket.accept()
        self.active_connections[game_id].append(websocket)

    def disconnect(self, websocket: WebSocket, game_id: str):
        if game_id in self.active_connections:
            self.active_connections[game_id] = [
                conn for conn in self.active_connections[game_id]
                if conn != websocket
            ]

    async def broadcast_game_update(self, game_id: str, game):
        if not self.redis:
            return

        message = json.dumps({
            "type": "game_update",
            "game": game.dict()
        })

        # Публикуем в Redis, чтобы все инстансы получили сообщение
        await self.redis.publish(f"game_updates:{game_id}", message)


ws_manager = WebSocketManager()