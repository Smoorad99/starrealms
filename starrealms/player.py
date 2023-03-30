"""Starrealms player module."""
import random
import typing as tp

from starrealms.action import (Action, AllyAbility, BuyCard, EndTurn, PlayCard,
                               ScrapCard)
from agents.agent import Agent
from starrealms.card import Card, CardType, CardAbility, CardFaction, Explorer, Scout, Viper, new

STARTING_AUTHORITY = 50
STARTING_SCOUTS = 8
STARTING_VIPERS = 2


class Player:
    def __init__(
        self,
        name: str,
        agent: Agent,
    ) -> None:
        """
        Store and control the player state

        Args:
            name: The name of the player
            select_action_callback: The callback function to select an action
        """
        self.name: str = name
        self.authority: int = STARTING_AUTHORITY
        self.trade: int = 0
        self.combat: int = 0
        self.hand: tp.List[Card] = []
        self.deck: tp.List[Card] = [new(Scout) for _ in range(STARTING_SCOUTS)] + [
            new(Viper) for _ in range(STARTING_VIPERS)
        ]
        self.discard: tp.List[Card] = []
        self.play_area: tp.List[Card] = []
        self.is_done: bool = True
        if agent:
            self.select_action: tp.Callable = agent.play
        self.moves: int = 0
        self.faction_played: tp.Dict[str, int] = {}

        random.shuffle(self.deck)

    def draw_cards(self, no_cards: int = 1) -> None:
        """Draw a card from the deck, handle an empty deck by shuffling the discard pile"""
        for _ in range(no_cards):
            if not self.deck:
                self.deck, self.discard = self.discard, []
                random.shuffle(self.deck)
            card = self.deck.pop(0)
            self.hand.append(card)


    def start_turn(self) -> None:
        """Start the player's turn"""
        self.is_done = False
        self.moves = 0
        for faction in CardFaction:
            self.faction_played[faction.value] = 0

    def end_turn(self):
        """End the player's turn"""
        self.is_done = True

    def finalize_turn(self):
        """Finalize the player's turn by cleaning up his hand an play area"""
        # All ship cards in play are discarded
        self.discard += self.hand
        self.hand = []
        # Only discard ships from play area
        self.discard += [card for card in self.play_area if card.type == CardType.SHIP]
        self.play_area = [card for card in self.play_area if card.type != CardType.SHIP]

        # Reset all card abilities
        for card in self.discard:
            for ability in card.abilities:
                ability.used = False
            if card.ally_abilities:
                for ability in card.ally_abilities:
                    ability.used = False
            if card.scrap_abilities:
                for ability in card.scrap_abilities:
                    ability.used = False

        # Discard rest of trade and reset combat
        self.trade = 0
        self.combat = 0
