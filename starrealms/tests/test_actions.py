# Test the actions available in the game
from starrealms.action import BuyCard, EndTurn, PlayCard, ScrapCard
from starrealms.card import Explorer, Viper, new
from starrealms.tests.fixtures import game, player1, player2


def test_play_card(game):
    """Test play card action"""
    game.player1.hand = [new(Viper)]

    PlayCard(game.player1.hand[0]).apply(game, game.player1)

    assert len(game.player1.play_area) == 1
    assert game.player1.play_area[0].name == "Viper"


def test_end_turn(game):
    """Test end turn action"""
    game.player1.start_turn()

    EndTurn().apply(game, game.player1)

    assert game.player1.is_done


def test_buy_card(game):
    """Test buy card from traderow action"""
    # Give player trade for this test
    game.player1.trade = 4

    # Select Explorer from traderow
    for card in game.trade_row:
        if card.name == "Explorer":
            BuyCard(card).apply(game, game.player1)
            break

    # Check that trade has been subtracted from player
    assert game.player1.trade == 2

    # Check that card is in player discard pile
    assert len(game.player1.discard) == 1
    assert game.player1.discard[0].name == "Explorer"


def test_scrap_card_explorer(game):
    """Test scrap card action for explorer"""
    card = new(Explorer)
    game.player1.play_area = [card]
    game.trade_row = []

    ScrapCard(card).apply(game, game.player1)

    # Check that the card has been placed back in the trade row
    assert len(game.trade_row) == 1
    assert game.trade_row[0].name == "Explorer"

    # Check that scrap ability was applied
    assert game.player1.combat == 2

    # Check that card is removed from play area
    assert len(game.player1.play_area) == 0
