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


def adversarial_search(
    problem: AdversarialSearchProblem[StateT, ActionT, PlayerT],
    state: StateT,
) -> ActionT | None:
    """
    Choose an action for the current game state.

    How your agent makes this choice is up to you.  You may add any helpers
    you find useful to this file, such as a heuristic, quiescence search,
    rollout policy, move ordering, or a cache.  None of those helpers is a
    required part of the submission interface.

    The ``problem`` object provides the game rules through methods including
    ``actions``, ``result``, ``to_move``, ``is_terminal``, and ``utility``.
    Your agent is responsible for choosing and managing its own search limits.

    Args:
        problem:
            The adversarial search problem.

        state:
            The current game state.

    Returns:
        The selected action: a zero-based column number from
        ``problem.actions(state)``.
        None if state is terminal or has no legal actions.

    Performance:
        Every call must return in less than 10 seconds.  Choose an internal
        search budget with enough margin to satisfy that hard limit.
    """
    

    """
    Hueristic Ideas:
    WE ARE MIN
    If we have 4 in a row, 0 because we've one
    If our opponent has 4 in a row, MAX because we've lost
    If our opponent has 3 in a rown with an opening on both sides, (MAX - 0.5) because they can win next turn
    If we have 3 in a row with an opening on both sides, 0.5 because we have a guarunteed win next turn
    If we have 3 in a row with one opening and they cannot block imediately, 1 because it could lead to a win
    
    board works left the right where left is the bottom
    """
    color = problem.to_move(state)
    heuristic_value = heuristic(state, color)
    raise NotImplementedError


def heuristic(state: StateT, computerColor) -> float:
    """
    Evaluate the given state and return a numeric score.

    The score should be higher for states that are better for the player whose
    turn it is to move.  The score should be lower for states that are worse
    for that player.

    Args:
        state:
            The game state to evaluate.
    """
    
    opponentColor = ""
    if computerColor == "Yellow":
        opponentColor = "Red"
    else:
        opponentColor = "Yellow"
    
    ##check for wins
    for col in range(7):
        for row in range(6):
            if state.columns[col][row] == computerColor:
                # Check horizontal
                if col <= 3 and all(state.columns[col + i][row] == computerColor for i in range(4)):
                    return 0.0  # Win
                # Check vertical
                if row <= 2 and all(state.columns[col][row + i] == computerColor for i in range(4)):
                    return 0.0  # Win
                # Check diagonal /
                if col <= 3 and row >= 3 and all(state.columns[col + i][row - i] == computerColor for i in range(4)):
                    return 0.0  # Win
                # Check diagonal \
                if col <= 3 and row <= 2 and all(state.columns[col + i][row + i] == computerColor for i in range(4)):
                    return 0.0  # Win

            if state.columns[col][row] == opponentColor:
                # Check horizontal
                if col <= 3 and all(state.columns[col + i][row] == opponentColor for i in range(4)):
                    return float("inf")  # Loss
                # Check vertical
                if row <= 2 and all(state.columns[col][row + i] == opponentColor for i in range(4)):
                    return float("inf")  # Loss
                # Check diagonal /
                if col <= 3 and row >= 3 and all(state.columns[col + i][row - i] == opponentColor for i in range(4)):
                    return float("inf")  # Loss
                # Check diagonal \
                if col <= 3 and row <= 2 and all(state.columns[col + i][row + i] == opponentColor for i in range(4)):
                    return float("inf")  # Loss

    


    val = state.columns[3][0]
    print(val)
    return 0.0



