from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src import crud, schemas

router = APIRouter()


@router.post("/", response_model=schemas.Game)
def create_game(game: schemas.GameCreate, db: Session = Depends(get_db)):
    # Проверяем существование игрока
    player = crud.get_player(db, game.creator_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    return crud.create_game(db, game, game.creator_id)


@router.get("/{game_id}", response_model=schemas.Game)
def read_game(game_id: str, db: Session = Depends(get_db)):
    db_game = crud.get_game(db, game_id)
    if not db_game:
        raise HTTPException(status_code=404, detail="Game not found")
    return db_game


@router.post("/{game_id}/move", response_model=schemas.Game)
def make_move_in_game(
        game_id: str,
        move: schemas.MoveRequest,
        db: Session = Depends(get_db)
):
    # Получаем игру
    db_game = crud.get_game(db, game_id)
    if not db_game:
        raise HTTPException(status_code=404, detail="Game not found")

    # Проверяем, что игрок участвует в игре
    player_in_game = any(
        player.player_id == move.player_id
        for player in db_game.players
    )
    if not player_in_game:
        raise HTTPException(status_code=403, detail="Player not in game")

    # Получаем текущее состояние
    game_state = schemas.GameState(**db_game.state)

    # Выполняем ход
    from src.services.game_service import make_move
    try:
        updated_state = make_move(game_state, move.player_id, move.x, move.y)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Обновляем состояние в БД
    updated_game = crud.update_game_state(db, game_id, updated_state)

    # Отправляем обновление через WebSocket
    from src.websockets.manager import ws_manager
    ws_manager.broadcast_game_update(game_id, updated_game)

    return updated_game