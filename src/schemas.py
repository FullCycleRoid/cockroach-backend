from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any


class PlayerBase(BaseModel):
    telegram_id: str
    username: Optional[str] = None
    first_name: str
    last_name: Optional[str] = None


class PlayerCreate(PlayerBase):
    pass


class Player(PlayerBase):
    created_at: datetime

    class Config:
        from_attributes = True


class GameState(BaseModel):
    cells: Dict[str, Dict[str, Any]]
    current_player: int
    remaining_moves: int
    activated_walls: List[str]
    is_game_over: bool
    winner: Optional[int] = None


class GameBase(BaseModel):
    id: str
    state: GameState
    current_player_id: str
    status: str
    winner_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class GameCreate(BaseModel):
    creator_id: str


class Game(GameBase):
    class Config:
        from_attributes = True


class GamePlayerBase(BaseModel):
    game_id: str
    player_id: str
    is_creator: bool


class GamePlayer(GamePlayerBase):
    class Config:
        from_attributes = True


class InviteBase(BaseModel):
    game_id: str
    player_id: str


class InviteCreate(InviteBase):
    pass


class Invite(InviteBase):
    id: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class MoveRequest(BaseModel):
    player_id: str
    x: int
    y: int