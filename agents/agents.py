"""Starrealms agent functions"""
import os
import random

from getch import getch

from starrealms.action import EndTurn
from agents.agent import Agent
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


