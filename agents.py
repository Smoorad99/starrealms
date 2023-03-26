"""Starrealms agent functions"""
import os
import random

import openai
from getch import getch

from starrealms.action import EndTurn
from starrealms.agent import Agent
from starrealms.card import CardFaction
from starrealms.interface import render, render_action


class RandomAgent(Agent):
    """
    Plays random actions
    """

    def play(self, game, actions):
        # Select random action
        selected_action_idx = random.randint(0, len(actions) - 1)
        action = actions[selected_action_idx]

        # Print the action that was selected in magenta followd by new line
        print(f"\033[1m\033[95m{render_action(action)}\033[0m")

        return action


class HumanAgent(Agent):
    """
    Human agent, the player controls its play using the terminal user interface
    """
    def __init__(self):
        self.play_all_neutral_turn = -1 

    def play(self, game, actions):
        # Create a list of letter keys in order of how easy they are to reach
        # The home row should be the first 10 keys followed by the next closest keys
        keys = "asdfghjklqwrtyuiopzxcvbnm"
        # Map keys to all actions except EndTurn
        key_action_map = {key: action for key, action in zip(keys, actions[:-1])}
        # Map the e to EndTurn
        key_action_map["e"] = actions[-1]

        render(game, actions, key_action_map)

        # Ask again if input was invalid
        while True:
            try:
                # If there is only end turn action left, auto select it
                if len(actions) == 1 and actions[0].__class__.__name__ == "EndTurn":
                    action = actions[0]
                    break

                print("Enter the index of the action you want to perform: ")
                print("(Press space to play all neutral cards on your turn)")

                # Early return if the agent is playing all neutral cards
                if self.play_all_neutral_turn == game.turn:
                    # Select the first PlayCard action that is associated with a card from a neutral faction 
                    for action in actions:
                        if action.__class__.__name__ == "PlayCard" and action.card.faction == CardFaction.NEUTRAL:
                            return action

                selected_action_key = getch()

                # If space is presed, set play_all_neutral_turn to the current turn
                # This will cause the agent to play all neutral cards on its turn
                if selected_action_key == " ":
                    self.play_all_neutral_turn = game.turn
                    continue

                # Get the action associated with the key
                action = key_action_map[selected_action_key]

            except KeyError:
                print("Invalid input. Please try again.")
            else:
                break

        # If this was Endturn, print an extra new line
        if isinstance(action, EndTurn):
            print()

        return action


class GPTAgent(Agent):
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if openai.api_key is None:
            raise ValueError("OPENAI_API_KEY is not set")

        self.preprompt = """
You are a starrealms player AI. 
You are playing against a human.
You want to win the game by reducing your opponents authority below 0 your own authority reaches zero.
You can play combat actions to decrease the authority of the opponent.
I will give you the current game state and a list of valid actions.
You will then select an action to perform. 
To select an action, only return the index of the action (action_index) as an integer.

Additional to the action index, you should also return the reason for your choice.
Your reasoning should be a short sentence in the tone of a smack talking cocky cow boy.

Your response should be in the following format:
action_index reason

The index should never exceed the highest action index.
The index should never be less than 0.

AI response:\n
"""

    def play(self, game, actions):
        game_state_prompt = f"""
Game State:
Draw Pile: {game.draw_pile}
Trade Row: {game.trade_row}
Discard Pile: {game.scrap_pile}
Authority: {game.current_player.authority}
Trade: {game.current_player.trade}
Combat: {game.current_player.combat}
Deck: {game.current_player.deck}
Hand: {game.current_player.hand}
In Play: {game.current_player.play_area}
Discard: {game.current_player.discard}
Opponent Authority: {game.opponent.authority}
Opponent Discard: {game.opponent.discard}
"""

        action_prompt = "List of actions:\n"
        for i, action in enumerate(actions):
            action_prompt += f"{i} {action}\n"
        action_prompt += f"Enter the index of the action you want to perform between 0 and {len(actions)}: "

        prompt = self.preprompt + "\n" + game_state_prompt + "\n" + action_prompt

        while True:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                temperature=0.5,
                max_tokens=64,
                top_p=1.0,
                frequency_penalty=0.5,
                presence_penalty=0.0,
            )

            try:
                response_text = response["choices"][0]["text"]
                action_idx = int(response_text.split(" ")[0])
                action = actions[action_idx]
            except IndexError:
                print(f"Thinking (index error)")
            except ValueError:
                print(f"Thinking (value error)")
            else:
                break

        try:
            reason = response_text.split(" ", 1)[1]
        except IndexError:
            reason = "I don't know why I did that."
        print(
            f"{action_idx} - \033[1m\033[95m{render_action(action)}\033[0m (\033[1m\033[90m{reason}\033[0m)"
        )

        return action


class GPTChatAgent(Agent):
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if openai.api_key is None:
            raise ValueError("OPENAI_API_KEY is not set")

        self.preprompt = """
You are a starrealms player AI. 
You are playing against a human.
You want to win the game by reducing your opponents authority below 0 your own authority reaches zero.
You can play combat actions to decrease the authority of the opponent.
I will give you the current game state and a list of valid actions.
You will then select an action to perform. 
To select an action, only return the index of the action (action_index) as an integer.

Additional to the action index, you should also return the reason for your choice.
Your reasoning should be a short concise and logical.

Your response should be in the following format:
action_index reason

The index should never exceed the highest action index.
The index should never be less than 0.
"""

        self.card_info_prompt = "Here are details and stratedgy for every card in the game:\n"
        self.card_info_prompt += """
Card: Explorer 
How to Play:
When you play Explorer, gain 2 Trade. At any time, you may scrap Explorer to gain 2 Combat.
Explorers are not shuffled into the main Trade deck. They are kept in a separate pile face up next to the Trade Row (opposite the Trade deck) where they are always available to be acquired.
When an Explorer is scrapped, it is placed back on top of the Explorer pile, not the scrap heap like other cards.
Strategy:
Explorers are a basic utility card always available to give your starting deck a trade boost, assuming there is nothing more cost effective in the Trade row. One important skill in the game is learning when mid game to stop buying Explorers and start scrapping them for the Combat bonus and to improve the efficiency of your deck.
"""
        self.card_info_prompt += """
Card: Scout 
How to Play:
When you play Scout, gain 1 Trade.
Strategy
Scouts are one of the two different cards each player has in their starting deck. One of the most crucial strategies in the game is scrapping the starter cards out of your deck to increase deck efficiency (i.e. increasing the odds of drawing other more powerful cards). It is a matter of personal preference (and some lively debate) whether it is best to scrap Vipers or Scouts first, but nevertheless the player who scraps starters the fastest is most often the winner.
"""
        self.card_info_prompt += """
Card: Viper 
How to Play:
When you play Viper, gain 1 Combat.
Strategy:
Vipers are one of the two different cards each player has in their starting deck. One of the most crucial strategies in the game is scrapping the starter cards out of your deck to increase deck efficiency (i.e. increasing the odds of drawing other more powerful cards). It is a matter of personal preference (and some lively debate) whether it is best to scrap Vipers or Scouts first, but nevertheless the player who scraps starters the fastest is most often the winner.
"""
        self.card_info_prompt += """
Card: Blob Fighter 
How to play:
When you play Blob Fighter, gain 3 Combat. At any time, if you have another Blob card in play, you may draw a card.
Strategy:
At one cost and 3 combat, Blob Fighter has the typical strong Blob combat value per trade cost. However the Blob Fighter really shines in a Blob-heavy deck when it can consistently trigger the draw and other Blob card's ally ability.
"""
        self.card_info_prompt += """
Card: Trade Pod 
How to Play:
When you play Trade Pod, gain 3 Trade. At any time, if you have a Blob card in play you may gain 2 Combat.
Strategy:
Two cost for three trade is a great deal that is very hard to pass up, especially in the first few turns of the game. As the game progresses, the value of the Trade Pod goes down, unless paired with haulers.
"""
        self.card_info_prompt += """
Card: Battle Pod 
How to Play:
When you play Battle Pod, gain 4 Combat and scrap one of the cards currently in the Trade Row. At any time, if you have another Blob card in play, you may gain 2 Combat.
Strategy:
The Battle Pod is a powerful "little" ship at 2 cost and 6 potential damage - great to counter an opponent's base in the early game.
However its real strength is in its ability to help control the trade row. Keep a close eye on what your opponent is buying and use the Battle Pod to keep strong combos away from him. If you know your opponent has a lot of trade, then it's probably good to clear the most powerful cards off the trade row. Also, if there is not a good option in the Trade Row for you to purchase, Battle Pod can help flip a better card for you to buy.
But be careful, sometimes you can flip an even better card for your opponent. Scrap with care!
"""
        self.card_info_prompt += """
Card: Ram 
How to Play:
When you play Ram, gain 5 Combat. At any time, if you have another Blob card in play, you may gain 2 Combat. Also, at any time you may scrap Ram to gain 3 Trade.
Strategy:
A typically powerful ship for the Blob faction, the Ram is great as an early buy. The Ram provides a lethal dose of damage and is often scrapped in the early game to purchase a more powerful card.
"""
        self.card_info_prompt += """
Card: Blob Destroyer 
How to Play:
When you play Blob Destroyer, gain 6 Combat. At any time, if you have another Blob card in play, you may choose to: destroy any base in play, or scrap a card in the trade row, or both.
Strategy:
With its 6 Combat for 4 cost, the Blob Destroyer makes a great early game buy for an "aggro" deck building strategy. When paired with other Blob cards, the Destroyer lives up to its name. It is an essential card when your opponent is playing a base strategy due to its ability to remove bases both with its ally ability and solid 6 Combat.
"""
        self.card_info_prompt += """
Card: Battle Blob 
How to Play:
When you play Battle Blob, gain 8 Combat. At any time, if you have another Blob card in play, you may draw a card. At any time, you may scrap Battle Blob to gain 4 Combat.Note: In the digital app, the ally ability is automatic and mandatory. However when playing with physical cards the ally ability is optional.
Strategy:
Battle Blob is a rather straightforward powerhouse card.  The 8 Combat and a possible draw alone makes the card well worth the 6 Trade cost in virtually any deck.  Where the true strategy comes in with Battle Blob is the scrap ability.  Normally the scrap is used in the end game either in the final turn, or when it is relatively certain given the number of cards remaining in your deck that you will not get a chance to play Battle Blob again.  Otherwise it is rarely scrapped during the mid game.
"""
        self.card_info_prompt += """
Card: Blob Carrier 
How to Play:
When you play Blob Carrier, gain 7 Combat. At any time, if you have another Blob card in play, you may acquire any ship without paying its cost and place it on top of your deck.
Strategy:
Typically strong 7 Combat as a Blob ship, this ship is usually a worthy buy at six cost, even if you're not likely to use it's ally ability. However it's ally ability is it's true strength. The ability to get any ship for free AND place it atop your deck (perhaps even play it the same turn with a draw ability) is incredibly powerful when you can trigger it consistently. Blob Carrier pairs well with any Blob card, Mech World, and Stealth Needle.
"""


    def play(self, game, actions):
        draw_pile = "Cards currently in draw pile:\n" 
        for card in game.draw_pile:
            draw_pile += f"{card.name}\n"
        draw_pile += "\n"

        trade_row = "Cards currently in trade row:\n"
        for card in game.trade_row:
            trade_row += f"{card.name}\n"
        trade_row += "\n"

        scrap_pile = "Cards currently in scrap pile:\n"
        for card in game.scrap_pile:
            scrap_pile += f"{card.name}\n"
        scrap_pile += "\n"

        current_player = "Current Player Information (yours):\n"
        current_player += f"Authority: {game.current_player.authority}\n"
        current_player += f"Trade: {game.current_player.trade}\n"
        current_player += f"Combat: {game.current_player.combat}\n"
        current_player += f"Deck: {len(game.current_player.deck)} cards\n"
        current_player += "\n"

        current_player_hand = "Current Player Hand (yours):\n"
        for card in game.current_player.hand:
            current_player_hand += f"{card.name}\n"
        current_player_hand += "\n"

        current_player_play_area = "Current Player Play Area (yours):\n"
        for card in game.current_player.play_area:
            current_player_play_area += f"{card.name}\n"
        current_player_play_area += "\n"

        current_player_discard = "Current Player Discard (yours):\n"
        for card in game.current_player.discard:
            current_player_discard += f"{card.name}\n"
        current_player_discard += "\n"

        opponent = "Opponent Information:\n"
        opponent += f"Authority: {game.opponent.authority}\n"
        opponent += f"Deck: {len(game.opponent.deck)} cards\n"
        opponent += "\n"

        opponent_discard = "Opponent Discard:\n"
        for card in game.opponent.discard:
            opponent_discard += f"{card.name}\n"
        opponent_discard += "\n"

        game_state_prompt = "Current Game State:"
        game_state_prompt += draw_pile
        game_state_prompt += trade_row
        game_state_prompt += scrap_pile
        game_state_prompt += current_player
        game_state_prompt += current_player_hand
        game_state_prompt += current_player_play_area
        game_state_prompt += current_player_discard
        game_state_prompt += opponent
        game_state_prompt += opponent_discard
        
        action_prompt = "List of actions indexes with their corrosponding actions:\n"
        for i, action in enumerate(actions):
            action_prompt += f"{i}"
            # Print out class name of action
            if action.__class__.__name__ == "PlayCard":
                action_prompt += f" Play {action.card.name} from hand into play area"
            elif action.__class__.__name__ == "BuyCard":
                action_prompt += f" Buy {action.card.name} from trade row"
            elif action.__class__.__name__ == "ScrapCard":
                action_prompt += f" Scrap {action.card.name} from play area"
            elif action.__class__.__name__ == "AllyAbility":
                action_prompt += f" Use ally abilities: {action.card.ally_abilities} of {action.card.name} in play area"
            elif action.__class__.__name__ == "PlayCardScrapTraderow":
                action_prompt += f" Scrap {action.traderow_card} from the traderow using {action.action.card.name} in hand"
            elif action.__class__.__name__ == "AcquireShip":
                action_prompt += f" Acquire {action.traderow_card} from the traderow and put ontop of your deck using {action.action.card.name}"
            elif action.__class__.__name__ == "ScrapTraderow":
                action_prompt += f" Scrap {action.traderow_card} from the traderow using {action.action.card.name} in play area"
            elif action.__class__.__name__ == "EndTurn":
                action_prompt += f" End Turn"
            else:
                raise NotImplementedError(f"Action {action.__class__.__name__} not implemented")
            action_prompt += "\n"
        action_prompt += f"Enter the index of the action you want to perform between 0 and {len(actions)-1} (inclusive): "

        while True:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "assistant", "content": self.preprompt},
                    {"role": "assistant", "content": self.card_info_prompt},
                    {"role": "assistant", "content": game_state_prompt},
                    {"role": "assistant", "content": action_prompt},
                    {
                        "role": "user",
                        "content": "Give me your answer strictly in the format `action reason`",
                    },
                ],
                temperature=0.0,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            )
            # print(response)

            try:
                response_text = response["choices"][0]["message"]["content"]
                action_idx = int(response_text.split(" ")[0])
                action = actions[action_idx]
            except IndexError:
                print(f"Thinking (index error)")
                print(f"{action_prompt=}\n{response_text=}")
            except ValueError:
                print(f"Thinking (value error)")
                print(f"{action_prompt=}\n{response_text=}")
            else:
                break

        try:
            reason = response_text.split(" ", 1)[1]
        except IndexError:
            reason = "I don't know why I did that."
        print(
            f"{action_idx} - \033[1m\033[95m{render_action(action)}\033[0m (\033[1m\033[90m{reason}\033[0m)"
        )

        return action
