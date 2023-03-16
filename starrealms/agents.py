"""Starrealms agent functions"""
import random

from starrealms.action import Action
from starrealms.game import Game
from starrealms.interface import render, render_action


def human_tui(game: Game, actions: Action):
    """
    Human agent, the player controls its play using the terminal user interface
    """
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
            selected_action_key = input(
                "Enter the index of the action you want to perform: "
            )
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


def random_play(game: Game, actions: Action, show: bool = False):
    """
    Plays random actions
    """
    if show:
        render(game, actions, key_action_map=None)

    # Select random action
    selected_action_idx = random.randint(0, len(actions) - 1)
    action = actions[selected_action_idx]

    # Print the action that was selected in magenta followd by new line
    print(f"\033[1m\033[95m{render_action(action)}\033[0m")

    return action
