import asyncio

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src import crud, schemas
from src.database import get_db
from src.services import game_service
from src.sockets.manager import ws_manager

router = APIRouter()


@router.post("/", response_model=schemas.GameResponse)
def create_game(game: schemas.GameCreate, db: Session = Depends(get_db)):
    player = crud.get_player(db, game.creator_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    db_game = crud.create_game(db, game.creator_id)
    return db_game


@router.get("/{game_id}", response_model=schemas.GameResponse)
def read_game(game_id: str, db: Session = Depends(get_db)):
    db_game = crud.get_game(db, game_id)
    if not db_game:
        raise HTTPException(status_code=404, detail="Game not found")
    return db_game


@router.post("/{game_id}/move", response_model=schemas.GameResponse)
def make_move_in_game(
    game_id: str, move: schemas.MoveRequest, db: Session = Depends(get_db)
):
    db_game = crud.get_game(db, game_id)
    if not db_game:
        raise HTTPException(status_code=404, detail="Game not found")

    # Проверка участия игрока
    player_in_game = any(p.player_id == move.player_id for p in db_game.players)
    if not player_in_game:
        raise HTTPException(status_code=403, detail="Player not in game")

    game_state = schemas.GameState(**db_game.state)

    try:
        # Обновляем состояние игры
        updated_state = game_service.make_move(
            game_state, move.player_id, db_game.players, move.x, move.y
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Сохраняем обновленное состояние
    updated_game = crud.update_game_state(db, game_id, updated_state)

    # Рассылаем обновление через WebSocket
    if updated_game:
        asyncio.create_task(ws_manager.broadcast_game_update(game_id, updated_game))

    return updated_game
