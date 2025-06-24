import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from src import models, schemas


def create_player(db: Session, player: schemas.PlayerCreate):
    db_player = models.Player(
        telegram_id=player.telegram_id,
        username=player.username,
        first_name=player.first_name,
        last_name=player.last_name,
    )
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player


def get_player(db: Session, telegram_id: str):
    return (
        db.query(models.Player).filter(models.Player.telegram_id == telegram_id).first()
    )


def create_game(db: Session, creator_id: str):
    game_id = str(uuid.uuid4())
    from src.services.game_service import initialize_game_state

    game_state = initialize_game_state()

    db_game = models.Game(id=game_id, state=game_state.dict(), status="waiting")
    db.add(db_game)

    # Добавляем создателя с номером 1
    db_game_player = models.GamePlayer(
        game_id=game_id, player_id=creator_id, is_creator=True, player_number=1
    )
    db.add(db_game_player)
    db.commit()
    db.refresh(db_game)
    return db_game


def get_game(db: Session, game_id: str):
    return db.query(models.Game).filter(models.Game.id == game_id).first()


def add_player_to_game(db: Session, game_id: str, player_id: str):
    game = get_game(db, game_id)
    if not game:
        return None

    # Проверяем количество игроков
    if len(game.players) >= 2:
        raise ValueError("Game is full")

    # Назначаем номер 2 новому игроку
    db_game_player = models.GamePlayer(
        game_id=game_id, player_id=player_id, is_creator=False, player_number=2
    )
    db.add(db_game_player)

    # Начинаем игру при наличии двух игроков
    if len(game.players) == 1:  # + новый игрок = 2
        game.status = "active"

    db.commit()
    return db_game_player


def create_invite(db: Session, invite: schemas.InviteCreate):
    invite_id = str(uuid.uuid4())
    db_invite = models.Invite(
        id=invite_id,
        game_id=invite.game_id,
        player_id=invite.player_id,
        status="pending",
    )
    db.add(db_invite)
    db.commit()
    db.refresh(db_invite)
    return db_invite


def get_invite(db: Session, invite_id: str):
    return db.query(models.Invite).filter(models.Invite.id == invite_id).first()


def accept_invite(db: Session, invite_id: str, player_id: str):
    invite = get_invite(db, invite_id)
    if invite and invite.player_id == player_id:
        invite.status = "accepted"
        add_player_to_game(db, invite.game_id, player_id)
        db.commit()
        return invite
    return None


def update_game_state(db: Session, game_id: str, game_state: schemas.GameState):
    game = get_game(db, game_id)
    if game:
        game.state = game_state.dict()
        game.updated_at = datetime.utcnow()

        if game_state.is_game_over:
            game.status = "finished"
            # Находим telegram_id победителя по номеру
            winner_number = game_state.winner
            winner_player = next(
                (p for p in game.players if p.player_number == winner_number), None
            )
            if winner_player:
                game.winner_id = winner_player.player_id

        db.commit()
        return game
    return None
