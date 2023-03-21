import typing as tp

def render_card(card):
    string = card.name
    # TODO: handle bases and outposts
    return string


def render_trade_row_card(card):
    # Render card with cost in yellow
    string = f"{render_card(card)}(\033[1m\033[93m{card.cost}\033[0m)"
    return string


def render_trade_row(game):
    # Render the trade row
    string = "\033[1mTrade Row:\033[0m "
    for card in game.trade_row:
        string += render_trade_row_card(card) + ", "
    return string


def render_hand(player):
    string = "\033[1mHand   :\033[0m "
    for card in player.hand:
        string += render_card(card) + ", "
    return string


def render_player(player):
    # Show player name in bold blue underlinee with name in uppercase
    string = f"\033[1m\033[4m\033[94m{player.name.upper()}\033[0m"
    # Show player authority, trade and combat next to name (authority, combat, trade),
    # trade should be in bold yellow, combat should be in bold red
    # authority should be in bold green
    string += f" [\033[1m\033[92mA:{player.authority}\033[0m, \033[1m\033[91mC:{player.combat}\033[0m, \033[1m\033[93mT:{player.trade}\033[0m]"
    string += "\n"
    # Render deck in bold
    string += f"\033[1mDeck   :\033[0m {len(player.deck)} | "
    # Render discard in bold
    string += f"\033[1mDiscard:\033[0m {len(player.discard)}"
    string += "\n"
    # Show the number of cards in hand
    string += render_hand(player)

    return string


def render_action(action):
    # Render name of action class
    string = f"\033[1m\033[97m{action.__class__.__name__}\033[0m"
    # Render card name if action has a card attribute
    if action.card:
        string += f" {render_card(action.card)}"
    return string


def render_actions_with_keys(key_action_map):
    # Render the actions in a numbered list
    string = ""
    for key, action in key_action_map.items():
        string += f"{key}: {render_action(action)}\n"
    return string


def render(game, actions, key_action_map):
    # Render the turn number in bold white cabital letters
    # Clear the terminal screen and go to top
    # print("\033[2J")
    # print("\033[0;0H")

    print(f"\n\033[1m\033[97mTURN {game.turn}\033[0m")
    print(render_player(game.player1))
    print()
    print(render_trade_row(game))
    print()
    print(render_player(game.player2))
    if key_action_map:
        print()
        print(render_actions_with_keys(key_action_map))
