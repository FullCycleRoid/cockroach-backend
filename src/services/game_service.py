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
    # Game rules implementation
    # 1. Placement must be within board boundaries
    if x < 0 or x >= 25 or y < 0 or y >= 30:
        return False

    # 2. Cell must be empty
    key = f"{x},{y}"
    if key in game_state.cells:
        return False

    # 3. Must be adjacent to own cockroach or wall
    if game_state.placed_roaches[player_number] == 0:
        # First placement - must be in base area
        center = 12
        if player_number == 1:
            return y < 8 and abs(x - center) <= 2
        else:
            return y > 21 and abs(x - center) <= 2
    else:
        # Subsequent placements
        adjacent_positions = [
            (x+1, y), (x-1, y), (x, y+1), (x, y-1),
            (x+1, y+1), (x-1, y-1), (x+1, y-1), (x-1, y+1)
        ]

        for ax, ay in adjacent_positions:
            akey = f"{ax},{ay}"
            if akey in game_state.cells:
                cell = game_state.cells[akey]
                if cell["player"] == player_number:
                    return True

                # Check if touching wall
                if cell["type"] == "wall":
                    return True

        return False


def make_move(game_state, player_id, game_players, x, y):
    # Get player number by player_id
    player = next((p for p in game_players if p.player_id == player_id), None)
    if not player or player.player_number != game_state.current_player:
        raise ValueError("Not player's turn")

    player_number = player.player_number
    key = f"{x},{y}"

    if game_state.phase == "placement":
        # Validate placement
        if not is_valid_placement(game_state, player_number, x, y):
            raise ValueError("Invalid placement position")

        # Place cockroach
        game_state.cells[key] = {
            "type": "x",
            "player": player_number
        }

        # Update counters
        game_state.placed_roaches[player_number] += 1

        # Check if both players have placed all cockroaches
        if (game_state.placed_roaches[1] >= 10 and
                game_state.placed_roaches[2] >= 10):
            game_state.phase = "activation"
            game_state.remaining_moves = 3
        else:
            # Switch player
            game_state.current_player = 3 - player_number
            game_state.remaining_moves = 1

    elif game_state.phase == "activation":
        # Validate activation
        if key in game_state.cells:
            raise ValueError("Cell already occupied")

        # Place wall
        game_state.cells[key] = {
            "type": "wall",
            "player": player_number
        }

        game_state.remaining_moves -= 1

        if game_state.remaining_moves <= 0:
            game_state.current_player = 3 - player_number
            game_state.remaining_moves = 3

    # Check for game over condition
    center = 12
    king1_key = f"{center},3"
    king2_key = f"{center},{30-4}"

    # Check if king is captured
    if (king1_key in game_state.cells and
            game_state.cells[king1_key]["player"] == 2):
        game_state.is_game_over = True
        game_state.winner = 2

    elif (king2_key in game_state.cells and
          game_state.cells[king2_key]["player"] == 1):
        game_state.is_game_over = True
        game_state.winner = 1

    return game_state
