from src.schemas import GameState


def initialize_game_state():
    return GameState(
        cells={},
        current_player=1,
        remaining_moves=1,
        activated_walls=[],
        is_game_over=False,
        winner=None,
        phase="placement",
        placed_roaches={1: 0, 2: 0}
    )


def is_valid_placement(game_state, player_number, x, y):
    # Проверка границ
    if x < 0 or x >= 25 or y < 0 or y >= 30:
        return False

    key = f"{x},{y}"
    if key in game_state.cells:
        return False

    # Для первого размещения - базовая зона
    if game_state.placed_roaches[player_number] == 0:
        center = 12
        if player_number == 1:
            return y < 8 and abs(x - center) <= 2
        else:
            return y > 21 and abs(x - center) <= 2

    # Для последующих - смежные позиции
    adjacent = [(x + dx, y + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx != 0 or dy != 0]

    for ax, ay in adjacent:
        if 0 <= ax < 25 and 0 <= ay < 30:
            akey = f"{ax},{ay}"
            cell = game_state.cells.get(akey)
            if cell:
                if cell.get("player") == player_number or cell.get("type") == "wall":
                    return True
    return False


def make_move(game_state, player_id, game_players, x, y):
    # Находим игрока и его номер
    player = next((p for p in game_players if p.player_id == player_id), None)
    if not player:
        raise ValueError("Player not found in game")

    player_number = player.player_number

    # Проверка очереди хода
    if player_number != game_state.current_player:
        raise ValueError("Not player's turn")

    key = f"{x},{y}"

    if game_state.phase == "placement":
        if not is_valid_placement(game_state, player_number, x, y):
            raise ValueError("Invalid placement position")

        game_state.cells[key] = {"type": "roach", "player": player_number}
        game_state.placed_roaches[player_number] += 1

        # Проверка завершения фазы размещения
        if all(count >= 10 for count in game_state.placed_roaches.values()):
            game_state.phase = "activation"
            game_state.remaining_moves = 3
        else:
            game_state.current_player = 3 - player_number
            game_state.remaining_moves = 1

    elif game_state.phase == "activation":
        if key in game_state.cells:
            raise ValueError("Cell already occupied")

        game_state.cells[key] = {"type": "wall", "player": player_number}
        game_state.remaining_moves -= 1

        if game_state.remaining_moves <= 0:
            game_state.current_player = 3 - player_number
            game_state.remaining_moves = 3

    # Проверка условий победы
    center = 12
    king_positions = {1: f"{center},3", 2: f"{center},26"}

    for pnum, pos in king_positions.items():
        cell = game_state.cells.get(pos)
        if cell and cell.get("player") != pnum:
            game_state.is_game_over = True
            game_state.winner = 3 - pnum
            break

    return game_state
