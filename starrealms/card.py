"""Starrealms card module"""
import typing as tp
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum

from starrealms.action import DrawCard


class CardType(Enum):
    SHIP = "ship"
    BASE = "base"
    OUTPOST = "outpost"


class CardAbility(Enum):
    COMBAT = "combat"
    TRADE = "trade"
    DRAW_CARD = "draw card"


class CardFaction(Enum):
    NEUTRAL = "neutral"
    BLOB = "blob"


class Ability:
    def __init__(self, ability: CardAbility, value: int):
        self.ability = ability
        self.value = value
        self.played = False

    def __repr__(self):
        return f"{self.ability.name}({self.value})"

    def use(self, game, player):
        if self.ability == CardAbility.COMBAT:
            player.combat += self.value
        if self.ability == CardAbility.TRADE:
            player.trade += self.value
        if self.ability == CardAbility.DRAW_CARD:
            DrawCard(self.value).apply(game, player)
        self.played = True


@dataclass
class Card:
    name: str
    cost: int
    faction: CardFaction
    ability: Ability
    type: CardType
    ally_ability: tp.Optional[Ability] = None
    scrap_ability: tp.Optional[Ability] = None

    def __str__(self):
        return f"{self.name}({self.cost})"

    def __repr__(self):
        return f"{self.name}(cost:{self.cost}, type:{self.type.name}, ability:{self.ability}, ally_ability:{self.ally_ability}, scrap_ability:{self.scrap_ability})"


def new(card: Card):
    return deepcopy(card)


"""
Card definitions
"""
Viper = Card(
    name="Viper",
    cost=0,
    faction=CardFaction.NEUTRAL,
    ability=Ability(CardAbility.COMBAT, 1),
    type=CardType.SHIP,
)

Scout = Card(
    name="Scout",
    cost=0,
    faction=CardFaction.NEUTRAL,
    ability=Ability(CardAbility.TRADE, 1),
    type=CardType.SHIP,
)

Explorer = Card(
    name="Explorer",
    cost=2,
    faction=CardFaction.NEUTRAL,
    ability=Ability(CardAbility.TRADE, 2),
    type=CardType.SHIP,
    scrap_ability=Ability(CardAbility.COMBAT, 2),
)

BlobFighter = Card(
    name="Blob Fighter",
    cost=1,
    faction=CardFaction.BLOB,
    ability=Ability(CardAbility.COMBAT, 2),
    type=CardType.SHIP,
    ally_ability=Ability(CardAbility.DRAW_CARD, 1),
)

TradePod = Card(
    name="Trade Pod",
    cost=2,
    faction=CardFaction.BLOB,
    ability=Ability(CardAbility.TRADE, 3),
    type=CardType.SHIP,
    ally_ability=Ability(CardAbility.COMBAT, 2),
)
