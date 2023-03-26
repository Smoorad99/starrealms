"""Starrealms card module"""
import typing as tp
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum

from starrealms.action import DrawCard

def create_blob_deck():
    cards = []
    for _ in range(3):
        cards.append(new(BlobFighter))
    for _ in range(3):
        cards.append(new(TradePod))
    for _ in range(2):
        cards.append(new(BattlePod))
    for _ in range(2):
        cards.append(new(Ram))
    for _ in range(2):
        cards.append(new(BlobDestroyer))
    cards.append(new(BattleBlob))
    cards.append(new(BlobCarrier))
    return cards
    


class CardType(Enum):
    SHIP = "ship"
    BASE = "base"
    OUTPOST = "outpost"


class CardAbility(Enum):
    COMBAT = "combat"
    TRADE = "trade"
    DRAW_CARD = "draw card"
    AUTHORITY = "authority"
    SCRAP_TRADEROW = "scrap traderow"
    DESTROY_BASE = "destroy base"
    ACQUIRE_SHIP = "acquire ship"


class CardFaction(Enum):
    NEUTRAL = "neutral"
    BLOB = "blob"


class Ability:
    def __init__(self, ability: CardAbility, value: int):
        self.ability = ability
        self.value = value
        self.played = False

    def __str__(self):
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
    abilities: tp.List[Ability]
    type: CardType
    ally_abilities: tp.Optional[tp.List[Ability]] = None 
    scrap_abilities: tp.Optional[tp.List[Ability]] = None 

    def __str__(self):
        return f"{self.name}(cost:{self.cost}, type:{self.type.name}, ability:{self.abilities}, ally_ability:{self.ally_abilities}, scrap_ability:{self.scrap_abilities})"


def new(card: Card):
    return deepcopy(card)


"""
Card definitions
"""
Viper = Card(
    name="Viper",
    cost=0,
    faction=CardFaction.NEUTRAL,
    abilities=[Ability(CardAbility.COMBAT, 1)],
    type=CardType.SHIP,
)

Scout = Card(
    name="Scout",
    cost=0,
    faction=CardFaction.NEUTRAL,
    abilities=[Ability(CardAbility.TRADE, 1)],
    type=CardType.SHIP,
)

Explorer = Card(
    name="Explorer",
    cost=2,
    faction=CardFaction.NEUTRAL,
    abilities=[Ability(CardAbility.TRADE, 2)],
    type=CardType.SHIP,
    scrap_abilities=[Ability(CardAbility.COMBAT, 2)],
)

BlobFighter = Card(
    name="Blob Fighter",
    cost=1,
    faction=CardFaction.BLOB,
    abilities=[Ability(CardAbility.COMBAT, 2)],
    type=CardType.SHIP,
    ally_abilities=[Ability(CardAbility.DRAW_CARD, 1)],
)

TradePod = Card(
    name="Trade Pod",
    cost=2,
    faction=CardFaction.BLOB,
    abilities=[Ability(CardAbility.TRADE, 3)],
    type=CardType.SHIP,
    ally_abilities=[Ability(CardAbility.COMBAT, 2)],
)

BattlePod = Card(
    name="Battle Pod",
    cost=2,
    faction=CardFaction.BLOB,
    abilities=[
        Ability(CardAbility.COMBAT, 4),
        Ability(CardAbility.SCRAP_TRADEROW, 1)
        ],   
    type=CardType.SHIP,
    ally_abilities=[Ability(CardAbility.COMBAT, 2)],
)

Ram = Card(
    name="Ram",
    cost=3,
    faction=CardFaction.BLOB,
    abilities=[Ability(CardAbility.COMBAT, 5)],
    type=CardType.SHIP,
    ally_abilities=[Ability(CardAbility.COMBAT, 2)],
    scrap_abilities=[Ability(CardAbility.TRADE, 3)],
)

BlobDestroyer = Card(
    name="Blob Destroyer",
    cost=4,
    faction=CardFaction.BLOB,
    abilities=[Ability(CardAbility.COMBAT, 6)],
    type=CardType.SHIP,
    ally_abilities=[Ability(CardAbility.DESTROY_BASE, 2), Ability(CardAbility.SCRAP_TRADEROW, 2)]
)

BattleBlob = Card(
    name="Battle Blob",
    cost=6,
    faction=CardFaction.BLOB,
    abilities=[Ability(CardAbility.COMBAT, 8)],
    type=CardType.SHIP,
    ally_abilities=[Ability(CardAbility.DRAW_CARD, 1)],
    scrap_abilities=[Ability(CardAbility.COMBAT, 4)]
)

BlobCarrier = Card(
    name="Blob Carrier",
    cost=6,
    faction=CardFaction.BLOB,
    abilities=[Ability(CardAbility.COMBAT, 7)],
    type=CardType.SHIP,
    ally_abilities=[Ability(CardAbility.ACQUIRE_SHIP, 1)],
)
