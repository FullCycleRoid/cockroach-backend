from backend.src.schemas import GameState


def initialize_game_state():
    # Ваша логика инициализации игры из React-компонента
    return GameState(
        cells={},
        current_player=1,
        remaining_moves=5,
        activated_walls=[],
        is_game_over=False,
        winner=None
    )


def make_move(game_state: GameState, player_id: str, x: int, y: int):
    # Здесь будет ваша игровая логика из React
    # Это упрощённый пример

    # Проверяем, что это ход текущего игрока
    current_player_num = 1 if game_state.current_player == player_id else 2
    if game_state.current_player != current_player_num:
        raise ValueError("Not player's turn")

    # Обновляем состояние игры
    # В реальности здесь будет ваша сложная логика

    # Пример обновления:
    key = f"{x},{y}"
    if key not in game_state.cells:
        game_state.cells[key] = {"type": "x", "player": current_player_num}

    # Уменьшаем количество оставшихся ходов
    game_state.remaining_moves -= 1

    # Если ходы закончились, передаём ход другому игроку
    if game_state.remaining_moves <= 0:
        game_state.current_player = 2 if game_state.current_player == 1 else 1
        game_state.remaining_moves = 5

    return game_state