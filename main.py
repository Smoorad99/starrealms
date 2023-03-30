from agents.agents import HumanAgent, RandomAgent
from agents.llm_agent import GPTChatAgent 
from starrealms.game import Game
from starrealms.player import Player

if __name__ == "__main__":
    player1 = Player("Player", HumanAgent())
    #player2 = Player("Ran Doe", RandomAgent())
    player2 = Player("GPT", GPTChatAgent())
    game = Game(player1, player2)
    print("Starting Game")
    game.play()
    winner = [player for player in game.players if player.authority > 0][0]
    # Print out winner in upper case bold green
    print(f"\033[1m\033[92m{winner.name.upper()} WINS!\033[0m")

# TODO: Provide opponent move list to agent
# TODO: Implement destroy outpost 
# TODO: store a log of the entire game
# FIXME: A bug where bases are not remaining in play
