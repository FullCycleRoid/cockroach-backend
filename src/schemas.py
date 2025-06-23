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
    cells: Dict[str, Dict[str, Any]] = {}
    current_player: int = 1
    remaining_moves: int = 10
    activated_walls: List[str] = []
    is_game_over: bool = False
    winner: Optional[int] = None
    phase: str = "placement"
    placed_roaches: Dict[int, int] = {1: 0, 2: 0}

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

class GamePlayerCreate(BaseModel):
    game_id: str
    player_id: str
    is_creator: bool = False
    player_number: Optional[int] = None

class GamePlayerResponse(BaseModel):
    game_id: str
    player_id: str
    is_creator: bool
    player_number: int
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