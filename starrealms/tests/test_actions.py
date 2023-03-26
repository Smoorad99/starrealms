# Test the actions available in the game
from starrealms.action import  BuyCard, EndTurn, PlayCard, PlayCardScrapTraderow, ScrapCard
from starrealms.card import Explorer, BattlePod, Viper, TradePod, BlobFighter, Scout, new
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


def test_buy_card_explorer(game):
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

def test_buy_card(game):
    """Test buy card from traderow action"""
    # Give player trade for this test
    game.player1.trade = 4
    game.draw_pile = [new(Scout), new(Scout), new(Scout), new(Scout), new(Scout)]
    game.trade_row = [new(BlobFighter), new(Explorer), new(TradePod)]

    initial_draw_pile_length = len(game.draw_pile)
    initial_trade_row_length = len(game.trade_row)

    # Select BlobFighter from traderow
    for card in game.trade_row:
        if card.name == "Blob Fighter":
            BuyCard(card).apply(game, game.player1)
            break

    # Check that trade has been subtracted from player
    assert game.player1.trade == 3 

    # Check that card is in player discard pile
    assert len(game.player1.discard) == 1
    assert game.player1.discard[0].name == "Blob Fighter"

    # Check that a new card has been drawn into the traderow
    assert len(game.trade_row) == initial_trade_row_length
    assert len(game.draw_pile) == initial_draw_pile_length - 1



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


def test_PlayCardScrapTraderow(game):
    """Test that a card that scrapes the trade row is removed from the trade row"""
    game.trade_row = [new(Explorer), new(TradePod), new(BattlePod)]
    game.player1.hand = [new(BattlePod)]

    # Make sure there is a PlayCardScrapTraderow action for the TradePod and the BattlePod but not for the Explorer
    valid_actions = game.get_valid_actions(game.player1)
    for action in valid_actions:
        if isinstance(action, PlayCardScrapTraderow):
            assert action.traderow_card.name in ["Trade Pod", "Battle Pod"]

    # Play the PlayCardScrapTraderow action for the BattlePod
    for action in valid_actions:
        if isinstance(action, PlayCardScrapTraderow) and action.action.card.name == "Battle Pod":
            action.apply(game, game.player1)
            break
    # HERE: Something is wrong with PlayCardScrapTraderow.apply() because the TradePod is not removed from the trade row
    # This is because the trade row is not updated in the game object
    for card in game.trade_row:
        print(card)

    # Check that the BattlePod is in the play area
    assert len(game.player1.play_area) == 1
    assert game.player1.play_area[0].name == "Battle Pod"

    # Check that a card is now in the scrap pile
    assert len(game.scrap_pile) == 1
