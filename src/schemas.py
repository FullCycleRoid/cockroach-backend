from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, field_validator


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
    cells: Dict[str, Dict[str, Any]] = {}
    current_player: int = 1
    remaining_moves: int = 1
    activated_walls: List[str] = []
    is_game_over: bool = False
    winner: Optional[int] = None
    phase: str = "placement"
    placed_roaches: Dict[int, int] = {1: 0, 2: 0}


class GameBase(BaseModel):
    id: str
    state: GameState
    status: str
    winner_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class GameCreate(BaseModel):
    creator_id: str


class GamePlayerBase(BaseModel):
    game_id: str
    player_id: str
    is_creator: bool
    player_number: int


class GamePlayerResponse(GamePlayerBase):
    player: Player

    class Config:
        from_attributes = True


class GameResponse(GameBase):
    players: List[GamePlayerResponse] = []

    class Config:
        from_attributes = True


class MoveRequest(BaseModel):
    player_id: str
    x: int
    y: int

    @field_validator("x", "y")
    def coordinates_must_be_valid(cls, v):
        if v < 0 or v > 30:
            raise ValueError("Coordinates must be between 0 and 30")
        return v


class InviteBase(BaseModel):
    game_id: str
    player_id: str


class InviteCreate(InviteBase):
    pass


class InviteResponse(InviteBase):
    id: str
    status: str
    created_at: datetime
    game: GameResponse
    player: Player

    class Config:
        from_attributes = True


class WebSocketMessage(BaseModel):
    type: str
    game: GameResponse
