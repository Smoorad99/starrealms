from starrealms.agents import human_tui, random_play
from starrealms.game import Game
from starrealms.player import Player

if __name__ == "__main__":
    player1 = Player("Player", human_tui)
    player2 = Player("Ran Doe", random_play)
    game = Game(player1, player2)
    print("Starting Game")
    game.play()
    winner = [player for player in game.players if player.authority > 0][0]
    # Print out winner in upper case bold green
    print(f"\033[1m\033[92m{winner.name.upper()} WINS!\033[0m")
