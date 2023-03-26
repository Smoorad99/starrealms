from agents import GPTAgent, GPTChatAgent, HumanAgent, RandomAgent
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

# TODO: Cleanup GPT agents
# TODO: Provide opponent move list to agent
# TODO: Provide information on every card to the agent
# TODO: Add cards
# TODO: Implement destroy base
# TODO: store a log of the entire game
# TODO: fix gpt action Scraptraderow action printout
