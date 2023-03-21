"""Starrealms agent functions"""
import os
import random

import openai
from getch import getch

from starrealms.action import EndTurn
from starrealms.agent import Agent
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
                print("Enter the index of the action you want to perform: ")
                selected_action_key = getch()

                # Get the action associated with the key
                action = key_action_map[selected_action_key]

                # If this was Endturn, print an extra new line
                if isinstance(action, EndTurn):
                    print()
            except KeyError:
                print("Invalid input. Please try again.")
            else:
                break

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
Your reasoning should be a short sentence in the tone of a smack talking cocky cow boy.

Your response should be in the following format:
action_index reason

The index should never exceed the highest action index.
The index should never be less than 0.
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
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "assistant", "content": prompt},
                    {
                        "role": "user",
                        "content": "Give me your answer strictly in the format `action reason` with no additional text. Never apologize",
                    },
                ],
                temperature=0.5,
                max_tokens=128,
                top_p=1.0,
                frequency_penalty=0.5,
                presence_penalty=0.0,
            )
            # print(response)

            try:
                response_text = response["choices"][0]["message"]["content"]
                action_idx = int(response_text.split(" ")[0])
                action = actions[action_idx]
            except IndexError:
                print(f"Thinking (index error)")
                print(response_text)
            except ValueError:
                print(f"Thinking (value error)")
                print(response_text)
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
