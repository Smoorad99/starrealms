# Test how the game reacts when playing cards

import pytest

from starrealms.action import AcquireShip, AllyAbility, EndTurn, PlayCard, ScrapCard, PlayCardScrapTraderow, ScrapTraderow, DestroyBase
from starrealms.card import Card, CardAbility, BattleBlob, BlobCarrier, BlobDestroyer, Ram, BlobFighter, Explorer, Scout, TradePod, BattlePod, Viper, new
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


def test_blob_fighter(game):
    """Test blob fighter card life cycle"""

    # Initialize the the turn for the current player
    # Remove all cards from the player hand for the test
    game.player1.start_turn()
    game.player1.hand = [new(BlobFighter)]

    PlayCard(game.player1.hand[0]).apply(game, game.player1)

    # Assert that the player has 1 blob fighter card in play
    assert len(game.player1.play_area) == 1
    assert game.player1.play_area[0].name == "Blob Fighter"
    assert game.player1.trade == 0
    assert game.player1.combat == 2

    # End and finalize the turn for the current player
    game.player1.finalize_turn()

    # Assert that the player has 1 blob fighter card in his discard pile
    assert len(game.player1.discard) == 1
    assert game.player1.discard[0].name == "Blob Fighter"
    assert game.player1.combat == 0


def test_blob_fighter_ally(game):
    """Test blob fighter card life cycle when ally"""

    # Initialize the the turn for the current player
    # Remove all cards from the player hand for the test
    game.player1.start_turn()
    game.player1.hand = [new(BlobFighter)]
    game.player1.deck = [new(Scout)]
    game.player1.play_area = [new(BlobFighter)]

    PlayCard(game.player1.hand[0]).apply(game, game.player1)

    # Assert that the player has 2 blob fighter card in play
    assert game.player1.trade == 0
    assert game.player1.combat == 2

    # Check that the valid action now contains an ally ability action
    valid_actions = game.get_valid_actions(game.player1)
    for action in valid_actions:
        if isinstance(action, AllyAbility):
            assert action.card.name == "Blob Fighter"
            # Take action
            action.apply(game, game.player1)
            break
    else:
        assert False

    # Check that a card was drawn
    assert len(game.player1.hand) == 1
    assert game.player1.hand[0].name == "Scout"
    assert len(game.player1.deck) == 0

    # Check that there is now only a single blob fighter ally ability left in the valid action list
    valid_actions = game.get_valid_actions(game.player1)
    count = 0
    for action in valid_actions:
        if isinstance(action, AllyAbility):
            assert action.card.name == "Blob Fighter"
            count += 1
    if count != 1:
        assert False

    # End and finalize the turn for the current player
    game.player1.finalize_turn()

    # The player should now have the scout, blob fighter and blob fighter in his discard pile
    assert len(game.player1.discard) == 3

    # Start player1 turn again
    game.player1.start_turn()
    # Move the blobfighters back to the play area from the discard pile
    for card in game.player1.discard:
        if card.name == "Blob Fighter":
            game.player1.play_area.append(card)
    # Get valid actions and make sure both AllyAbilities are available again.
    # Abilities are reset the moment the turn ends
    valid_actions = game.get_valid_actions(game.player1)
    count = 0
    for action in valid_actions:
        if isinstance(action, AllyAbility):
            assert action.card.name == "Blob Fighter"
            count += 1
    if count != 2:
        assert False
    # TODO: These ally ability played tests should go in test_actions


def test_card_tradepod(game):
    """Test tradepod card life cycle"""

    # Initialize the the turn for the current player
    # Remove all cards from the player hand for the test
    game.player1.start_turn()
    game.player1.hand = [new(TradePod), new(TradePod)]

    PlayCard(game.player1.hand[0]).apply(game, game.player1)

    assert game.player1.trade == 3
    assert game.player1.combat == 0

    # Play second tradepod
    PlayCard(game.player1.hand[0]).apply(game, game.player1)

    assert game.player1.trade == 6

    # Play ally ability
    valid_actions = game.get_valid_actions(game.player1)
    for action in valid_actions:
        if isinstance(action, AllyAbility):
            assert action.card.name == "Trade Pod"
            # Take action
            action.apply(game, game.player1)
            break

    # Check that the player combat is now 2
    assert game.player1.combat == 2

    # End and finalize the turn for the current player
    game.player1.finalize_turn()


def test_card_battlepod(game):
    """Test battlepod card life cycle"""
    game.player1.start_turn()
    game.player1.hand = [new(BattlePod), new(BattlePod)]

    # Put a blob fighter and a scout in the trade row
    game.trade_row = [new(BlobFighter), new(Scout)]
    game.draw_pile = [new(Viper), new(Viper), new(Viper)]

    # We expect there to be a PlayCardScrapTradeRow action in the valid actions list
    # for each available traderow card that can be scrapped. The original PlayCard
    # action should be gone
    valid_actions = game.get_valid_actions(game.player1)
    found_playcardscraptraderow = 0
    found_playcard = 0
    for action in valid_actions:
        if isinstance(action, PlayCardScrapTraderow):
            found_playcardscraptraderow += 1 
        if isinstance(action, PlayCard):
            found_playcard += 1
    if found_playcardscraptraderow != 4:
        assert False
    if found_playcard != 2:
        assert False

    # Take the PlayCardScrapTradeRow action for the blob fighter
    for action in valid_actions:
        if isinstance(action, PlayCardScrapTraderow):
            if action.action.card.name == "Battle Pod":
                action.apply(game, game.player1)
                break

    # Make sure the blob fighter is not in the traderow and has been moved to 
    # the scrap pile
    assert len(game.trade_row) == 2 
    # Make sure there is atleast 1 scout and 1 viper in the traderow
    assert len([card for card in game.trade_row if card.name == "Scout"]) == 1
    assert len([card for card in game.trade_row if card.name == "Viper"]) == 1
    assert len(game.scrap_pile) == 1
    assert game.scrap_pile[0].name == "Blob Fighter"

    assert game.player1.trade == 0
    assert game.player1.combat == 4 

    # Play second battlepod without using the scrap ability by finding and playing the PlayCard action
    valid_actions = game.get_valid_actions(game.player1)
    for action in valid_actions:
        if isinstance(action, PlayCard):
            if action.card.name == "Battle Pod":
                action.apply(game, game.player1)
                break

    assert game.player1.combat == 8

    # Play ally ability
    valid_actions = game.get_valid_actions(game.player1)
    for action in valid_actions:
        if isinstance(action, AllyAbility):
            assert action.card.name == "Battle Pod"
            action.apply(game, game.player1)
            break

    assert game.player1.combat == 10

def test_card_ram(game):
    """Test ram card life cycle"""
    game.player1.start_turn()
    game.player1.hand = [new(Ram), new(BattlePod)]

    # Play the ram card
    actions = game.get_valid_actions(game.player1)
    for action in actions:
        if isinstance(action, PlayCard):
            if action.card.name == "Ram":
                action.apply(game, game.player1)
                break

    # Check combat increase
    assert game.player1.combat == 5 

    # Play the battlepod card
    actions = game.get_valid_actions(game.player1)
    for action in actions:
        if isinstance(action, PlayCard):
            if action.card.name == "Battle Pod":
                action.apply(game, game.player1)
                break

    # Play ally ability of Ram
    actions = game.get_valid_actions(game.player1)
    for action in actions:
        if isinstance(action, AllyAbility):
            if action.card.name == "Ram":
                action.apply(game, game.player1)
                break

    # Check combat increase
    assert game.player1.combat == 11 
    
    # Trash the ram
    actions = game.get_valid_actions(game.player1)
    for action in actions:
        if isinstance(action, ScrapCard):
            if action.card.name == "Ram":
                action.apply(game, game.player1)
                break

    assert len(game.player1.play_area) == 1 
    assert game.player1.play_area[0].name == "Battle Pod"
    assert len(game.scrap_pile) == 1
    assert game.player1.trade == 3 

def test_card_blob_destroyer(game):
    """Test blob destroyer life cycle"""
    game.player1.start_turn()
    game.player1.hand = [new(BlobDestroyer), new(BattlePod)]
    game.trade_row = []
    
    # At this point there should be 2 available PlayCard actions
    actions = game.get_valid_actions(game.player1)
    assert len(actions) == 3 

    game.trade_row = [new(BlobFighter)]

    # Play the blob destroyer
    actions = game.get_valid_actions(game.player1)

    # There should only be 4 actions
    assert len(actions) == 4 

    for action in actions:
        if isinstance(action, PlayCard):
            if action.card.name == "Blob Destroyer":
                action.apply(game, game.player1)
                break

    # Check combat increase
    assert game.player1.combat == 6 

    # Play the battlepod card
    actions = game.get_valid_actions(game.player1)
    for action in actions:
        if isinstance(action, PlayCard):
            if action.card.name == "Battle Pod":
                action.apply(game, game.player1)
                break

    # Check that there is atleast 1 ally ability from the blob destroyer
    # the ability should contain one destroy base and one trade row scrap ability
    actions = game.get_valid_actions(game.player1)
    found_destroy_base = 0
    found_trade_row_scrap = 0
    for action in actions:
        if isinstance(action, AllyAbility) and action.card.name == "Blob Destroyer":
            for ability in action.card.ally_abilities:
                if ability.ability == CardAbility.DESTROY_BASE:
                    found_destroy_base += 1
                if ability.ability == CardAbility.SCRAP_TRADEROW:
                    found_trade_row_scrap += 1
    assert found_destroy_base == 2 
    assert found_trade_row_scrap == 2 

    # Make sure there is a scrap traderow action for the blob fighter
    for action in actions:
        if isinstance(action, ScrapTraderow):
            assert action.traderow_card.name == "Blob Fighter"
            break
    else:
        assert False

    game.trade_row = [new(Explorer)]

    actions = game.get_valid_actions(game.player1)
    # Make sure there are no ScrapCard actions for explorers available  
    actions = game.get_valid_actions(game.player1)
    for action in actions:
        if isinstance(action, ScrapTraderow):
            assert action.traderow_card.name != "Explorer"
    
def test_card_battleblob(game):
    """Test the lifecycle of the battleblob card"""
    game.player1.start_turn()
    game.player1.hand = [new(BattleBlob)]
    game.player1.deck = [new(Scout)]
    game.trade_row = []

    # Play battleblob
    actions = game.get_valid_actions(game.player1)
    for action in actions:
        if isinstance(action, PlayCard):
            if action.card.name == "Battle Blob":
                action.apply(game, game.player1)
                break

    # Check combat increase
    assert game.player1.combat == 8 

    # Check that there is only end turn and scrap action available
    actions = game.get_valid_actions(game.player1)
    for action in actions:
        print(action)
    assert len(actions) == 2 

    # Add another blob to play area
    game.player1.play_area.append(new(BlobFighter))

    # Make sure Battle Blob ally ability is now available
    actions = game.get_valid_actions(game.player1)
    for action in actions:
        if isinstance(action, AllyAbility):
            assert action.card.name == "Battle Blob"
            break
    else:
        assert False

    # Play battle blob ally ability
    for action in actions:
        if isinstance(action, AllyAbility):
            if action.card.name == "Battle Blob":
                action.apply(game, game.player1)
                break

    # Check that a scout has been drawn from deck into hand
    assert len(game.player1.deck) == 0
    assert len(game.player1.hand) == 1
    assert game.player1.hand[0].name == "Scout"

    # Play the battle blob scrap action
    actions = game.get_valid_actions(game.player1)
    for action in actions:
        if isinstance(action, ScrapCard):
            if action.card.name == "Battle Blob":
                action.apply(game, game.player1)
                break

    # Check that battle blob is now in the scrap pile, combat increase and the
    # battle blob is not in play anymore
    assert len(game.scrap_pile) == 1
    assert game.scrap_pile[0].name == "Battle Blob"
    assert game.player1.combat == 12 
    assert len(game.player1.play_area) == 1
    assert game.player1.play_area[0].name == "Blob Fighter"

def test_only_PlayCard_actions_should_get_PlayCardScrapTraderow_actions(game):
    game.player1.start_turn()
    game.player1.hand = []
    game.player1.deck = []
    game.trade_row = [new(Explorer), new(BattleBlob), new(BattleBlob), new(BlobDestroyer), new(BattlePod)]
    game.player1.trade = 10

    # Check that there is no PlayCardScrapTradeRow actions
    actions = game.get_valid_actions(game.player1)
    for action in actions:
        assert not isinstance(action, PlayCardScrapTraderow)

def test_card_blob_carrier(game):
    """Test lifecycle of blob carrier"""
    game.player1.start_turn()
    game.player1.hand = [new(BlobCarrier)]
    game.player1.deck = [new(BlobFighter), new(BattleBlob)]
    game.trade_row = [new(Explorer), new(BattlePod)]

    # Play blob carrier
    actions = game.get_valid_actions(game.player1)
    for action in actions:
        if isinstance(action, PlayCard):
            if action.card.name == "Blob Carrier":
                action.apply(game, game.player1)
                break

    # Check combat increase
    assert game.player1.combat == 7 

    # Add another blob in the play area and check if Acquire ship actions are given
    game.player1.play_area.append(new(BlobFighter))

    actions = game.get_valid_actions(game.player1)
    for action in actions:
        print(action)
    # There should be 2 AcquireShip actions, 1 BattleBlob and 1 BlobFighter
    found_explorer = 0
    found_battlepod = 0
    for action in actions:
        if isinstance(action, AcquireShip):
            print(action.traderow_card)
            if action.traderow_card.name == "Explorer":
                found_explorer += 1
            if action.traderow_card.name == "Battle Pod":
                found_battlepod += 1
    assert found_explorer == 1 
    assert found_battlepod == 1 
    # Make sure the AllyAbility action has been removed for AcquireShip actions
    for action in actions:
        if isinstance(action, AllyAbility):
            assert action.card.name != "Blob Carrier"

    # Play the AcquireShip action for the explorer
    for action in actions:
        if isinstance(action, AcquireShip):
            if action.traderow_card.name == "Explorer":
                action.apply(game, game.player1)
                break
    # Make sure the explorer is not in the traderow anymore
    for card in game.trade_row:
        assert card.name != "Explorer"
    # Make sure the Explorer is now on top of the player deck
    assert len(game.player1.deck) == 3
    assert game.player1.deck[0].name == "Explorer"
