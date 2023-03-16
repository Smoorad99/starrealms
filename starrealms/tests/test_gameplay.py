# Test the gameplay of the game
from starrealms.action import EndTurn, PlayCard
from starrealms.card import Viper, new
from starrealms.tests.fixtures import game, player1, player2


def test_gamesetup(game):
    """Test that the game is setup correctly"""

    # Check that the trade row has 10 explorers
    assert len([c for c in game.trade_row if c.name == "Explorer"]) == 10

    # Check that each player has 8 scouts and 2 vipers combined in hand and deck
    assert (
        len([c for c in game.player1.hand + game.player1.deck if c.name == "Scout"])
        == 8
    )
    assert (
        len([c for c in game.player2.hand + game.player2.deck if c.name == "Scout"])
        == 8
    )
    assert (
        len([c for c in game.player1.hand + game.player1.deck if c.name == "Viper"])
        == 2
    )
    assert (
        len([c for c in game.player2.hand + game.player2.deck if c.name == "Viper"])
        == 2
    )

    # Check that player 1 has 3 cards in his hand and play area is empty
    assert len(game.player1.hand) == 3
    assert len(game.player1.play_area) == 0

    # Check that player 2 has 5 cards in his hand and play area is empty
    assert len(game.player2.hand) == 5
    assert len(game.player2.play_area) == 0

    # Check that each player has 50 authority
    for player in game.players:
        assert player.authority == 50

    # First player to start is player 1
    assert game.current_player_idx == 0


def test_first_turn(game):
    """In the first turn, player 1 draws 3 cards into his hand from his deck"""

    def select_callback(game, valid_actions):
        # Check that it is now player 1's turn
        assert game.current_player.name == "Player 1"
        # Check that the player has drawn 3 cards into his hand
        assert len(game.current_player.hand) == 3
        # Check that the player deck now only has 7 cards
        assert len(game.current_player.deck) == 7
        # Check that the discard pile and play area are empty
        assert len(game.current_player.discard) == 0
        # Check that the player has 3 PlayCard actions
        assert len([a for a in valid_actions if isinstance(a, PlayCard)]) == 3
        # Check that the player has 1 EndTurn action
        assert len([a for a in valid_actions if isinstance(a, EndTurn)]) == 1

        # Return the end turn action
        return [a for a in valid_actions if isinstance(a, EndTurn)][0]

    game.player1.select_action = select_callback
    game.player2.select_action = select_callback

    game.tick()

    # Check that the current player is now player 2
    assert game.current_player_idx == 1

    # Check that there are now 3 cards in player 1 discard pile
    assert len(game.player1.discard) == 3


def test_second_turn(game):
    """Similar to the first turn, but this time its player 2 and he draws 5 cards"""
    test_turn = 2

    def select_callback(game, valid_actions):
        if game.turn == test_turn:
            # Check that the player has drawn 5 cards into his hand
            assert len(game.current_player.hand) == 5
            # Check that the player deck now only has 5 cards
            assert len(game.current_player.deck) == 5
            # Check that the discard pile and play area are empty
            assert len(game.current_player.discard) == 0

        # Return the end turn action
        return [a for a in valid_actions if isinstance(a, EndTurn)][0]

    game.player1.select_action = select_callback
    game.player2.select_action = select_callback

    for _ in range(test_turn):
        game.tick()

    # Check that the current player is now player 1
    assert game.current_player_idx == 0

    # Check that there are now 5 cards in player 2 discard pile
    assert len(game.player2.discard) == 5


def test_third_turn(game):
    """Similar to the second turn, but this time its player 1 his discard pile is shuffled into his deck"""
    test_turn = 3

    def select_callback(game, valid_actions):
        if game.turn == test_turn:
            # Check that the player has drawn 5 cards into his hand
            assert len(game.current_player.hand) == 5
            # Check that the player deck now only has 5 cards
            assert len(game.current_player.deck) == 2  # Drew 3 and now 5 leaving 2
            # Check that the discard pile has the 3 cards from the first turn
            assert len(game.current_player.discard) == 3

        # Return the end turn action
        return [a for a in valid_actions if isinstance(a, EndTurn)][0]

    game.player1.select_action = select_callback
    game.player2.select_action = select_callback

    for _ in range(test_turn):
        game.tick()

    assert len(game.player1.discard) == 0


def test_fourth_turn(game):
    """Similar to the third turn, but this time its player 2 and he draws 5 cards"""
    test_turn = 4

    def select_callback(game, valid_actions):
        if game.turn == test_turn:
            # Check that the player has drawn 5 cards into his hand
            assert len(game.current_player.hand) == 5
            # Check that the player deck now has 0 cards
            assert len(game.current_player.deck) == 0  # Drew 5 and now 5 leaving 0
            # Check that the discard pile has the 5 cards from the second turn
            assert len(game.current_player.discard) == 5

        # Return the end turn action
        return [a for a in valid_actions if isinstance(a, EndTurn)][0]

    game.player1.select_action = select_callback
    game.player2.select_action = select_callback

    for _ in range(test_turn):
        game.tick()

    # Check that there are now 0 cards in player 2 discard pile
    assert len(game.player2.discard) == 0


def test_combat(game):
    """Test that combat works correctly"""

    def select_callback(game, valid_actions):
        # Check if hand contains a card
        if len(game.current_player.hand) > 0:
            return PlayCard(game.current_player.hand[0])
        else:
            return EndTurn()

    game.player1.select_action = select_callback
    game.player1.hand = [new(Viper)]

    game.tick()

    # Check that player 2 now has reduced authority
    assert game.player2.authority == 49
