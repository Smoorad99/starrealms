# Test how the game reacts when playing cards

# HERE:
# Test playing a scout card
# Test playing a viper card
# Test playing an explorer card

import pytest

from starrealms.action import EndTurn, PlayCard, ScrapCard
from starrealms.card import Explorer, Scout, Viper, new
from starrealms.tests.fixtures import game, player1, player2


def test_card_scout(game):
    """Test scout card life cycle"""

    # Initialize the the turn for the current player
    # Remove all cards from the player hand for the test
    game.player1.start_turn()
    game.player1.hand = [new(Scout)]

    PlayCard(game.player1.hand[0]).apply(game, game.player1)

    # Assert that the player has 1 scout card in play
    assert len(game.player1.play_area) == 1
    assert game.player1.play_area[0].name == "Scout"
    assert game.player1.trade == 1
    assert game.player1.combat == 0

    # End and finalize the turn for the current player
    game.player1.finalize_turn()

    # Assert that the player has 1 scout card in his discard pile
    assert len(game.player1.discard) == 1
    assert game.player1.discard[0].name == "Scout"
    assert game.player1.trade == 0


def test_card_viper(game):
    """Test viper card life cycle"""

    # Initialize the the turn for the current player
    # Remove all cards from the player hand for the test
    game.player1.start_turn()
    game.player1.hand = [new(Viper)]

    PlayCard(game.player1.hand[0]).apply(game, game.player1)

    # Assert that the player has 1 scout card in play
    assert len(game.player1.play_area) == 1
    assert game.player1.play_area[0].name == "Viper"
    assert game.player1.trade == 0
    assert game.player1.combat == 1

    # End and finalize the turn for the current player
    game.player1.finalize_turn()

    # Assert that the player has 1 scout card in his discard pile
    assert len(game.player1.discard) == 1
    assert game.player1.discard[0].name == "Viper"
    assert game.player1.combat == 0


def test_card_explorer(game):
    """Test explorer card life cycle"""

    # Initialize the the turn for the current player
    # Remove all cards from the player hand for the test
    game.player1.start_turn()
    game.player1.hand = [new(Explorer)]
    game.trade_row = []

    PlayCard(game.player1.hand[0]).apply(game, game.player1)

    # Assert that the player has 1 explorer card in play
    assert len(game.player1.play_area) == 1
    assert game.player1.play_area[0].name == "Explorer"
    assert game.player1.trade == 2
    assert game.player1.combat == 0

    # Check that the player has the explorer scrap action in its valid actions
    valid_actions = game.get_valid_actions(game.player1)
    for action in valid_actions:
        if isinstance(action, ScrapCard):
            assert action.card.name == "Explorer"
            break
    else:
        assert False

    # Check that combat has been added to combat pool
    assert game.player1.combat == 0

    # End and finalize the turn for the current player
    game.player1.finalize_turn()

    # Check that the explore is back in the players discard pile
    assert len(game.player1.discard) == 1
    assert game.player1.discard[0].name == "Explorer"


def test_card_explorer_scrap(game):
    """Test explorer card life cycle when scrapped"""

    # Initialize the the turn for the current player
    # Remove all cards from the player hand for the test
    game.player1.start_turn()
    game.player1.hand = [new(Explorer)]
    game.trade_row = []

    PlayCard(game.player1.hand[0]).apply(game, game.player1)

    # Check that the player has the explorer scrap action in its valid actions
    valid_actions = game.get_valid_actions(game.player1)
    for action in valid_actions:
        if isinstance(action, ScrapCard):
            assert action.card.name == "Explorer"
            action.apply(game, game.player1)
            break
    else:
        assert False

    # Make sure the explorer card is placed back into the trade row
    assert len(game.trade_row) == 1
    assert game.trade_row[0].name == "Explorer"
    assert game.player1.play_area == []

    # Check that combat has been added to combat pool
    assert game.player1.combat == 2

    # End and finalize the turn for the current player
    game.player1.finalize_turn()

    # Check that there is no explorer in the player discard pile
    assert len(game.player1.discard) == 0
