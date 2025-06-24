from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src.sockets.manager import ws_manager

router = APIRouter()


@router.websocket("/game/{game_id}")
async def websocket_game_endpoint(websocket: WebSocket, game_id: str):
    await ws_manager.connect(websocket, game_id)
    try:
        while True:
            # Keep connection alive, no need to process messages
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, game_id)
    except Exception as e:
        print(f"WebSocket error: {e}")
        ws_manager.disconnect(websocket, game_id)
