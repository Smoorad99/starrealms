"""Starrealms card module"""
import typing as tp
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum


class CardType(Enum):
    SHIP = "ship"
    BASE = "base"
    OUTPOST = "outpost"


class CardAbility(Enum):
    COMBAT = "combat"
    TRADE = "trade"


@dataclass
class Card:
    name: str
    cost: int
    abilities: tp.Dict[CardAbility, int]
    type: CardType
    scrap_abilities: tp.Optional[tp.Dict[CardAbility, int]] = None

    def __str__(self):
        return f"{self.name}({self.cost})"

    def __repr__(self):
        return f"{self.name}(cost:{self.cost}, type:{self.type.name}, abilities:{self.abilities}, scrap_abilities:{self.scrap_abilities})"


def new(card: Card):
    return deepcopy(card)


"""
Card definitions
"""
Viper = Card(
    name="Viper", cost=0, abilities={CardAbility.COMBAT: 1}, type=CardType.SHIP
)

Scout = Card(name="Scout", cost=0, abilities={CardAbility.TRADE: 1}, type=CardType.SHIP)

Explorer = Card(
    name="Explorer",
    cost=2,
    abilities={CardAbility.TRADE: 2},
    type=CardType.SHIP,
    scrap_abilities={CardAbility.COMBAT: 2},
)
