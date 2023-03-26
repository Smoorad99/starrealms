import random
import typing as tp

from starrealms.action import AcquireShip, AllyAbility, ScrapCard, EndTurn, PlayCard, BuyCard, PlayCardScrapTraderow, ScrapTraderow, DestroyBase
from starrealms.card import Card, CardType, CardFaction, CardAbility, Explorer, new, create_blob_deck
from starrealms.player import Player

PLAYER1_STARTING_CARDS = 3
PLAYER2_STARTING_CARDS = 5


class Game:
    def __init__(self, player1: Player, player2: Player):
        """
        Store and control the starrealm game state

        Args:
            player1: The first player
            player2: The second player
        """
        self.player1: Player = player1
        self.player2: Player = player2
        self.players: tp.Tuple[Player, Player] = (player1, player2)

        self.trade_row: tp.List[Card] = []
        self.draw_pile: tp.List[Card] = []
        self.scrap_pile: tp.List[Card] = []

        self.initialize_game_state()
        self.current_player_idx: int = 0
        self.turn: int = 0

        self.current_player: Player = self.players[self.current_player_idx]
        self.opponent: Player = self.players[1 - self.current_player_idx]

        # Draw initial cards 
        self.draw_traderow_cards(5)
        player1.draw_cards(PLAYER1_STARTING_CARDS)
        player2.draw_cards(PLAYER2_STARTING_CARDS)

    def initialize_game_state(self):
        """Initialize the game state by setting up the draw pile and traderow"""
        self.draw_pile = create_blob_deck()
        random.shuffle(self.draw_pile)
        self.trade_row = [new(Explorer) for _ in range(10)]

    def tick(self):
        """Perform a single game tick"""
        self.current_player = self.players[self.current_player_idx]
        self.opponent = self.players[1 - self.current_player_idx]
        self.current_player.start_turn()

        # Main Phase
        # Do any of the following
        # 1. Play a card from hand
        # 2. Use primary abilities of inplay bases
        # 3. Use the ally and scrap abilities of in play bases and ships
        # 4. Use acquired trade to buy ships from the trade row
        # 5. Use acquired combat to attack oppoenent and or their bases
        while True:
            valid_actions = self.get_valid_actions(self.current_player)
            action = self.current_player.select_action(self, valid_actions)
            action.apply(self, self.current_player)

            if self.current_player.is_done:
                break

        # Discard phase
        # Use remaining combat points on opponent
        # Put all in play ships into discard pile
        # Put all cards in hand into discard pile
        self.opponent.authority -= self.current_player.combat
        self.current_player.finalize_turn()

        # Draw phase
        # Draw 5 cards
        self.current_player.draw_cards(5)

        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
        self.turn += 1

    def get_valid_actions(self, player: Player) -> list:
        """Return a list of valid actions for the player regarding the traderow"""
        actions = []

        # Get a count for how many of each faction is in play
        faction_counts = {faction: 0 for faction in CardFaction}
        for card in player.play_area:
            faction_counts[card.faction] += 1

        # Add purchase card actions from trade row
        for card in self.trade_row:
            # Check if the card is affordable
            if card.cost <= player.trade:
                actions.append(BuyCard(card))

        # Add hand play card actions
        for card in player.hand:
            actions.append(PlayCard(card))

        # Check if a hand PlayCard action has a SCRAP_TRADEROW ability
        # In this case we need to expand the PlayCard action
        # into additional PlayCardTradRowScrapActions
        for action in actions:
            if isinstance(action, PlayCard):
                for ability in action.card.abilities:
                    if ability.ability == CardAbility.SCRAP_TRADEROW:
                        for traderow_card in self.trade_row:
                            if traderow_card.name != "Explorer":
                                actions.append(PlayCardScrapTraderow(action, traderow_card))

        # Add actions for play area cards
        for card in player.play_area:
            # Add trash action if this card has the ability 
            if card.scrap_abilities:
                actions.append(ScrapCard(card))

            # Add ally abilities actions for cards in play
            if card.ally_abilities and faction_counts[card.faction] > 1:
                for ability in card.ally_abilities: 
                    if not ability.played:
                        actions.append(AllyAbility(card))

        for action in actions:
            if isinstance(action, AllyAbility):
                for ability in action.card.ally_abilities:
                    # For all SCRAP_TRADEROW abilities in ally abilities, 
                    # append a ScrapTraderow action
                    if ability.ability == CardAbility.SCRAP_TRADEROW:
                        for traderow_card in self.trade_row:
                            # Cannot trash explorers
                            if traderow_card.name != "Explorer":
                                actions.append(ScrapTraderow(action, traderow_card))
                    # For all ACQUIRE_SHIP abilities in ally abilities, 
                    # append a AcquireShip action
                    if ability.ability == CardAbility.ACQUIRE_SHIP:
                        for traderow_card in self.trade_row:
                            actions.append(AcquireShip(action, traderow_card))
        # Remove AllyAbility actions with AcquireShip abilities
        actions = [action for action in actions if not (isinstance(action, AllyAbility) and any(ability.ability == CardAbility.ACQUIRE_SHIP for ability in action.card.ally_abilities))]


        # Check if an action has the DESTROY_BASE ability
        # We need to add DestroyBase actions to the list for every opponent base
        #for action in actions:
        #    if hasattr(action, "card"):
        #        for ability in action.card.abilities:
        #            if ability.ability == CardAbility.DESTROY_BASE:
        #                # For every opponent in play card check if it is of type base
        #                for opponent_card in self.opponent.in_play:
        #                    if opponent_card.type == CardType.BASE:
        #                        actions.append(DestroyBase(action, opponent_card))

        actions.append((EndTurn()))

        return actions

    def draw_traderow_cards(self, n: int):
        """Draw n cards from the traderow"""
        for _ in range(n):
            if not self.draw_pile:
                self.draw_pile = self.scrap_pile
                self.scrap_pile = []
                random.shuffle(self.draw_pile)
            else:
                self.trade_row.append(self.draw_pile.pop())


    def check_game_over(self) -> bool:
        """Check if the game is over"""
        return any(player.authority <= 0 for player in self.players)

    def play(self):
        """Play the game until it is over"""
        while not self.check_game_over():
            self.tick()
