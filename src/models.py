from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from src.database import Base

class Player(Base):
    __tablename__ = "players"
    telegram_id = Column(String, primary_key=True, index=True)
    username = Column(String, nullable=True)
    first_name = Column(String)
    last_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    games = relationship("GamePlayer", back_populates="player")
    invites = relationship("Invite", back_populates="player")

class Game(Base):
    __tablename__ = "games"
    id = Column(String, primary_key=True, index=True)
    state = Column(JSON)
    current_player_id = Column(String)
    status = Column(String, default="waiting")
    winner_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    players = relationship("GamePlayer", back_populates="game")
    invites = relationship("Invite", back_populates="game")

class GamePlayer(Base):
    __tablename__ = "game_players"
    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(String, ForeignKey("games.id"))
    player_id = Column(String, ForeignKey("players.telegram_id"))
    is_creator = Column(Boolean, default=False)
    player_number = Column(Integer, nullable=True)  # 1 or 2
    game = relationship("Game", back_populates="players")
    player = relationship("Player", back_populates="games")

class Invite(Base):
    __tablename__ = "invites"
    id = Column(String, primary_key=True, index=True)
    game_id = Column(String, ForeignKey("games.id"))
    player_id = Column(String, ForeignKey("players.telegram_id"))
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    game = relationship("Game", back_populates="invites")
    player = relationship("Player", back_populates="invites")