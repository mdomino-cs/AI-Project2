"""Student implementations for CS 4341 Assignment 2."""
from __future__ import annotations

# Import utilities
try:
    from .adversarial_search import (
        ActionT,
        AdversarialSearchProblem,
        PlayerT,
        StateT,
    )
except ImportError:
    from adversarial_search import (
        ActionT,
        AdversarialSearchProblem,
        PlayerT,
        StateT,
    )


# Replace this with the name your group wants displayed in the tournament.
GROUP_NAME = "Mike & Matt"


def minimax(
    problem: AdversarialSearchProblem[StateT, ActionT, PlayerT],
    state: StateT,
    depth: int,
    root_player: PlayerT,
) -> float:
    return 0


def adversarial_search(
    problem: AdversarialSearchProblem[StateT, ActionT, PlayerT],
    state: StateT,
) -> ActionT | None:
    """Choose the best legal move using a shallow minimax search."""
    legal_actions = list(problem.actions(state))
    if not legal_actions:
        return None

    root_player = problem.to_move(state)
    depth = 4  # maximum plies to search from root

    best_move: ActionT | None = None
    best_score = float("inf")

    for action in legal_actions:
        child = problem.result(state, action)
        score = minimax(problem, child, depth - 1, root_player)
        if score < best_score:
            best_score = score
            best_move = action

    return best_move


def heuristic(state: StateT, computerColor) -> float:
    """
    Evaluate the given state and return a numeric score.

    Lower is better for the player whose turn it is to move; higher values mean
    the position is worse for that player.
    """

    opponentColor = "Red" if computerColor == "Yellow" else "Yellow"

    def cell(column: int, row: int):
        if 0 <= column < 7 and 0 <= row < 6:
            column_cells = state.columns[column]
            if row < len(column_cells):
                return column_cells[row]
        return None

    # Immediate wins/losses.
    for col in range(7):
        for row in range(6):
            if row >= len(state.columns[col]):
                continue
            current = state.columns[col][row]

            if current == computerColor:
                if col <= 3 and all(cell(col + i, row) == computerColor for i in range(4)):
                    return -1_000_000.0
                if row <= 2 and all(cell(col, row + i) == computerColor for i in range(4)):
                    return -1_000_000.0
                if col <= 3 and row >= 3 and all(cell(col + i, row - i) == computerColor for i in range(4)):
                    return -1_000_000.0
                if col <= 3 and row <= 2 and all(cell(col + i, row + i) == computerColor for i in range(4)):
                    return -1_000_000.0

            if current == opponentColor:
                if col <= 3 and all(cell(col + i, row) == opponentColor for i in range(4)):
                    return 1_000_000.0
                if row <= 2 and all(cell(col, row + i) == opponentColor for i in range(4)):
                    return 1_000_000.0
                if col <= 3 and row >= 3 and all(cell(col + i, row - i) == opponentColor for i in range(4)):
                    return 1_000_000.0
                if col <= 3 and row <= 2 and all(cell(col + i, row + i) == opponentColor for i in range(4)):
                    return 1_000_000.0

    # Open-ended three-in-a-row threats.
    for col in range(7):
        for row in range(6):
            for dc, dr in ((1, 0), (0, 1), (1, 1), (1, -1)):
                cells = [cell(col + dc * i, row + dr * i) for i in range(5)]
                if cells.count(opponentColor) == 3 and cells.count(None) == 2:
                    if cells[0] is None and cells[-1] is None:
                        return 500.0
                if cells.count(computerColor) == 3 and cells.count(None) == 2:
                    if cells[0] is None and cells[-1] is None:
                        return -500.0

    # Three-in-a-row with one opening (possible immediate follow-up).
    for col in range(7):
        for row in range(6):
            for dc, dr in ((1, 0), (0, 1), (1, 1), (1, -1)):
                cells = [cell(col + dc * i, row + dr * i) for i in range(4)]
                if cells.count(opponentColor) == 3 and cells.count(None) == 1:
                    if cells[0] is None or cells[-1] is None:
                        return 100.0
                if cells.count(computerColor) == 3 and cells.count(None) == 1:
                    if cells[0] is None or cells[-1] is None:
                        return -100.0

    # Fallback: prefer center pieces because they are stronger in Connect Four.
    center_score = 0.0
    for col in range(7):
        center_weight = 3 - abs(col - 3)
        for row in range(6):
            value = cell(col, row)
            if value == computerColor:
                center_score -= center_weight
            elif value == opponentColor:
                center_score += center_weight

    return center_score



