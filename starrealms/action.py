"""Starrealms action module"""
from enum import Enum

from starrealms.card import Card, CardAbility


class ActionType(Enum):
    PLAY = "play"
    BUY = "buy"
    SCRAP = "scrap"
    END_TURN = "end turn"


class Action:
    card = None

    def apply(self, game, player):
        pass


class PlayCard(Action):
    def __init__(self, card: Card):
        self.card = card

    def apply(self, game, player):
        player.hand.remove(self.card)
        player.play_area.append(self.card)

        # If card has trade ability add trade points to player
        for ability, value in self.card.abilities.items():
            if ability == CardAbility.TRADE:
                player.trade += value
            if ability == CardAbility.COMBAT:
                player.combat += value


class BuyCard(Action):
    def __init__(self, card: Card):
        self.card = card

    def apply(self, game, player):
        game.trade_row.remove(self.card)
        player.discard.append(self.card)
        player.trade -= self.card.cost


class ScrapCard(Action):
    def __init__(self, card: Card):
        self.card = card

    def apply(self, game, player):
        player.play_area.remove(self.card)

        # Handle scrap abilities
        if self.card.scrap_abilities:
            for ability, value in self.card.scrap_abilities.items():
                if ability == CardAbility.TRADE:
                    player.trade += value
                if ability == CardAbility.COMBAT:
                    player.combat += value

        # If this is an explorer add it back to the trade row
        if self.card.name == "Explorer":
            game.trade_row.append(self.card)
        else:
            game.scrap_pile.append(self.card)


class EndTurn(Action):
    def apply(self, game, player):
        player.end_turn()
