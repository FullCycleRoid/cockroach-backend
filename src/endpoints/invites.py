from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src import schemas, crud
from src.database import get_db
from src.services import telegram_service

router = APIRouter()


@router.post("/", response_model=schemas.Invite)
def create_invite(invite: schemas.InviteCreate, db: Session = Depends(get_db)):
    # Проверяем существование игрока
    player = crud.get_player(db, invite.player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    # Проверяем существование игры
    game = crud.get_game(db, invite.game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    # Создаём приглашение
    db_invite = crud.create_invite(db, invite)

    # Отправляем уведомление через Telegram
    creator = next(
        (gp.player for gp in game.players if gp.is_creator),
        None
    )

    if creator:
        telegram_service.send_invite_notification(
            player.telegram_id,
            game.id,
            creator.username
        )

    return db_invite


@router.post("/{invite_id}/accept", response_model=schemas.Game)
def accept_invite(invite_id: str, player_id: str, db: Session = Depends(get_db)):
    db_invite = crud.accept_invite(db, invite_id, player_id)
    if not db_invite:
        raise HTTPException(status_code=404, detail="Invite not found or already accepted")

    return crud.get_game(db, db_invite.game_id)