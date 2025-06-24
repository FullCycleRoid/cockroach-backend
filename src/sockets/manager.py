import asyncio
from collections import defaultdict

import redis.asyncio as redis
from fastapi import WebSocket

from src.schemas import WebSocketMessage


class WebSocketManager:
    def __init__(self):
        self.active_connections = defaultdict(list)
        self.redis = None
        self.pubsub = None

    async def connect_redis(self):
        from src.config import settings

        try:
            self.redis = redis.Redis.from_url(
                settings.REDIS_URL,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_keepalive=True,
            )
            await self.redis.ping()
            self.pubsub = self.redis.pubsub()
            asyncio.create_task(self.listen_redis())
            print("✅ Connected to Redis")
            return True
        except Exception as e:
            print(f"❌ Redis connection error: {e}")
            return False

    async def disconnect_redis(self):
        try:
            if self.pubsub:
                await self.pubsub.close()
            if self.redis:
                await self.redis.close()
            print("🔌 Disconnected from Redis")
        except Exception as e:
            print(f"Redis disconnect error: {e}")

    async def listen_redis(self):
        await self.pubsub.psubscribe("game_updates:*")
        print("👂 Listening for Redis pub/sub messages")

        async for message in self.pubsub.listen():
            if message["type"] == "pmessage":
                try:
                    channel = message["channel"]
                    game_id = channel.split(":")[1]
                    data = message["data"]

                    # Send update to all connected clients for this game
                    for connection in self.active_connections.get(game_id, []):
                        try:
                            await connection.send_text(data)
                        except Exception as e:
                            print(f"WebSocket send error: {e}")
                            self.disconnect(connection, game_id)
                except Exception as e:
                    print(f"Error processing Redis message: {e}")

    async def connect(self, websocket: WebSocket, game_id: str):
        await websocket.accept()
        self.active_connections[game_id].append(websocket)
        print(f"🔗 WebSocket connected for game {game_id}")

    def disconnect(self, websocket: WebSocket, game_id: str):
        if game_id in self.active_connections:
            self.active_connections[game_id] = [
                conn for conn in self.active_connections[game_id] if conn != websocket
            ]
            print(f"🔌 WebSocket disconnected for game {game_id}")

    async def broadcast_game_update(self, game_id: str, game):
        if not self.redis:
            return False

        try:
            message = WebSocketMessage(type="game_update", game=game)
            message_json = message.json()

            # Publish to Redis for all instances
            await self.redis.publish(f"game_updates:{game_id}", message_json)

            # Send directly to connected clients
            for connection in self.active_connections.get(game_id, []):
                try:
                    await connection.send_text(message_json)
                except Exception as e:
                    print(f"Direct WebSocket send error: {e}")
                    self.disconnect(connection, game_id)

            return True
        except Exception as e:
            print(f"Broadcast error: {e}")
            return False


ws_manager = WebSocketManager()
