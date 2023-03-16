import pytest

from starrealms.game import Game
from starrealms.player import Player


@pytest.fixture
def player1():
    return Player("Player 1", None)


@pytest.fixture
def player2():
    return Player("Player 2", None)


@pytest.fixture
def game(player1, player2):
    return Game(player1, player2)
