from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src import crud, schemas
from src.database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.Player)
def create_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    db_player = crud.get_player(db, player.telegram_id)
    if db_player:
        return db_player
    return crud.create_player(db, player)


@router.get("/{telegram_id}", response_model=schemas.Player)
def read_player(telegram_id: str, db: Session = Depends(get_db)):
    db_player = crud.get_player(db, telegram_id)
    if not db_player:
        raise HTTPException(status_code=404, detail="Player not found")
    return db_player


@router.get("/{telegram_id}/games", response_model=list[schemas.GameResponse])
def get_player_games(telegram_id: str, db: Session = Depends(get_db)):
    player = crud.get_player(db, telegram_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    # Get all games where player is participating
    return [gp.game for gp in player.games if gp.game.status != "waiting"]
