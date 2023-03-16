import random
import typing as tp

from starrealms.card import Card, Explorer, new
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

        # Players draw their initial cards
        player1.draw_cards(PLAYER1_STARTING_CARDS)
        player2.draw_cards(PLAYER2_STARTING_CARDS)

    def initialize_game_state(self):
        """Initialize the game state by setting up the draw pile and traderow"""
        self.draw_pile = []
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

        # Purchase cards from trade row
        for card in self.trade_row:
            # Check if the card is affordable
            if card.cost <= player.trade:
                actions.append(BuyCard(card))

        actions += player.valid_actions()

        return actions

    def check_game_over(self) -> bool:
        """Check if the game is over"""
        return any(player.authority <= 0 for player in self.players)

    def play(self):
        """Play the game until it is over"""
        while not self.check_game_over():
            self.tick()
