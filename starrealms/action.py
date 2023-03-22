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
    def __init__(self, card):
        self.card = card

    def apply(self, game, player):
        player.hand.remove(self.card)
        player.play_area.append(self.card)

        self.card.ability.use(game, player)

    def __repr__(self) -> str:
        return f"PlayCard({self.card.__repr__()})"


class BuyCard(Action):
    def __init__(self, card):
        self.card = card

    def apply(self, game, player):
        game.trade_row.remove(self.card)
        player.discard.append(self.card)
        player.trade -= self.card.cost

    def __repr__(self) -> str:
        return f"ScrapCard({self.card.__repr__()})"


class ScrapCard(Action):
    def __init__(self, card):
        self.card = card

    def apply(self, game, player):
        player.play_area.remove(self.card)

        # Handle scrap abilities
        if self.card.scrap_ability:
            self.card.scrap_ability.use(game, player)

        # If this is an explorer add it back to the trade row
        if self.card.name == "Explorer":
            game.trade_row.append(self.card)
        else:
            game.scrap_pile.append(self.card)

    def __repr__(self) -> str:
        return f"ScrapCard({self.card.__repr__()})"


class DrawCard(Action):
    def __init__(self, card):
        self.card = card

    def apply(self, game, player):
        player.draw_cards(1)

    def __repr__(self) -> str:
        return f"DrawCard({self.card.__repr__()})"


class AllyAbility(Action):
    def __init__(self, card):
        self.card = card

    def apply(self, game, player):
        self.card.ally_ability.use(game, player)

    def __repr__(self) -> str:
        return f"AllyAbility({self.card}-{self.card.ally_ability.__repr__()})"


class EndTurn(Action):
    def apply(self, game, player):
        player.end_turn()

    def __repr__(self) -> str:
        return "EndTurn()"
