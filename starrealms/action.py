"""Starrealms action module"""
from enum import Enum


class ActionType(Enum):
    PLAY = "play"
    BUY = "buy"
    SCRAP = "scrap"
    END_TURN = "end turn"


class Action:
    def apply(self, game, player):
        pass


class PlayCard(Action):
    def __init__(self, card, abilities=None):
        self.card = card
        # If abilities are not specified, use all abilities on card
        self.abilities = abilities if abilities else card.abilities

    def apply(self, game, player):
        player.hand.remove(self.card)
        player.play_area.append(self.card)
        player.faction_played[self.card.faction.value] += 1

        for ability in self.abilities:
            ability.use(game, player)

    def __str__(self) -> str:
        return f"PlayCard({self.card}: {self.abilities})"

class ScrapTraderow(Action):
    def __init__(self, action, traderow_card):
        self.action = action 
        self.traderow_card = traderow_card

    def apply(self, game, player):
        # Scrap the trade row card
        card = game.trade_row.pop(game.trade_row.index(self.traderow_card))
        game.scrap_pile.append(card)
        game.draw_traderow_cards(1)

    def __str__(self) -> str:
        return f"ScrapTraderow({self.action}-{self.action.card}: {self.traderow_card})"


# Special action for cards that can scrap trade row cards in their main ability
# These actions are created during gameplay as needed
class PlayCardScrapTraderow(Action):
    def __init__(self, action, traderow_card):
        self.action = action 
        self.traderow_card = traderow_card

    def apply(self, game, player):
        player.hand.remove(self.action.card)
        player.play_area.append(self.action.card)
        player.faction_played[self.action.card.faction.value] += 1

        for ability in self.action.card.abilities:
            ability.use(game, player)

        # Scrap the trade row card
        card = game.trade_row.pop(game.trade_row.index(self.traderow_card))
        game.scrap_pile.append(card)
        game.draw_traderow_cards(1)

    def __str__(self) -> str:
        return f"PlayCardScrapTraderow({self.action}: {self.traderow_card})"


class AcquireShip(Action):
    def __init__(self, action, traderow_card):
        self.action = action 
        self.traderow_card = traderow_card

    def apply(self, game, player):
        # Place the card ontop of the player deck 
        card = game.trade_row.pop(game.trade_row.index(self.traderow_card))
        # The card should be the first card to be drawn when calling pop
        player.deck.insert(0, self.traderow_card)
        game.draw_traderow_cards(1)

    def __str__(self) -> str:
        return f"AcquireShip({self.action}: {self.traderow_card})"


class DestroyBase(Action):
    def __init__(self, base_card, card=None):
        self.card = card
        self.base = base_card

    def apply(self, game, player):
        game.opponent.play_area.remove(self.base)
        game.opponent.discard.append(self.base)

        if not self.card:
            player.combat -= self.base.shield

        

    def __str__(self) -> str:
        return f"DestroyBase({self.card}: {self.base})"


class BuyCard(Action):
    def __init__(self, card):
        self.card = card

    def apply(self, game, player):
        game.trade_row.remove(self.card)
        player.discard.append(self.card)
        player.trade -= self.card.cost
        game.draw_traderow_cards(1)

    def __str__(self) -> str:
        return f"BuyCard({self.card})"


class ScrapCard(Action):
    def __init__(self, card):
        self.card = card

    def apply(self, game, player):
        player.play_area.remove(self.card)

        # Handle scrap abilities
        for ability in self.card.scrap_abilities:
            ability.use(game, player)

        # If this is an explorer add it back to the trade row
        if self.card.name == "Explorer":
            game.trade_row.append(self.card)
        else:
            game.scrap_pile.append(self.card)

    def __str__(self) -> str:
        return f"ScrapCard({self.card})"


class DrawCard(Action):
    def __init__(self, no_cards):
        self.no_cards = no_cards

    def apply(self, game, player):
        player.draw_cards(self.no_cards)

    def __str__(self) -> str:
        return f"DrawCard({self.no_cards})"


class AllyAbility(Action):
    def __init__(self, card, ability):
        self.card = card
        self.ability = ability

    def apply(self, game, player):
        self.ability.use(game, player)

    def __str__(self) -> str:
        return f"AllyAbilitty({self.card}-{self.card.ally_abilities})"


class EndTurn(Action):
    def apply(self, game, player):
        player.end_turn()

    def __str__(self) -> str:
        return "EndTurn()"
