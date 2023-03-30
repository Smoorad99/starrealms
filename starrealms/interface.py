import typing as tp
from starrealms.card import CardFaction, CardAbility, Ability

def render_card(card):
    if card == None:
        return "None"

    string = card.name

    if card.faction == CardFaction.NEUTRAL:
        # If card is a neutral card, render it in magenta
        string = f"\033[1m\033[95m{string}\033[0m"
    if card.faction == CardFaction.BLOB:
        # If card is a blob card, render it in green 
        string = f"\033[1m\033[92m{string}\033[0m"

    # Render abilities 
    string += " ("
    if card.abilities:
        # FIXME: update and cleanup
        for ability in card.abilities:
            if isinstance(ability, Ability):
                if ability.ability == CardAbility.COMBAT:
                    string += f"\033[1m\033[91m{ability.value}\033[0m, "
                if ability.ability == CardAbility.TRADE:
                    string += f"\033[1m\033[93m{ability.value}\033[0m, "
                if ability.ability == CardAbility.DRAW_CARD:
                    string += f"\033[1m\033[97mdraw {ability.value}\033[0m, "
                if ability.ability == CardAbility.AUTHORITY:
                    string += f"\033[1m\033[92m{ability.value}\033[0m, "

    # Render ally abilities
    string = string[:-2] +"| "
    if card.ally_abilities:
        # Render ally abilities in [ally1, ally2, ...]
        for ability in card.ally_abilities:
            if isinstance(ability, Ability):
                if ability.ability == CardAbility.COMBAT:
                    string += f"\033[1m\033[91m{ability.value}\033[0m, "
                if ability.ability == CardAbility.TRADE:
                    string += f"\033[1m\033[93m{ability.value}\033[0m, "
                if ability.ability == CardAbility.DRAW_CARD:
                    string += f"\033[1m\033[97mdraw {ability.value}\033[0m, "
                if ability.ability == CardAbility.AUTHORITY:
                    string += f"\033[1m\033[92m{ability.value}\033[0m, "
    # Render scrap abilities
    string = string[:-2] +"| "
    if card.scrap_abilities:
        for ability in card.scrap_abilities:
            if isinstance(ability, Ability):
                if ability.ability == CardAbility.COMBAT:
                    string += f"\033[1m\033[91m{ability.value}\033[0m, "
                if ability.ability == CardAbility.TRADE:
                    string += f"\033[1m\033[93m{ability.value}\033[0m, "
                if ability.ability == CardAbility.DRAW_CARD:
                    string += f"\033[1m\033[97mdraw {ability.value}\033[0m, "
                if ability.ability == CardAbility.AUTHORITY:
                    string += f"\033[1m\033[92m{ability.value}\033[0m, "
    string = string[:-2] + ")"

    # TODO: handle bases and outposts
    return string


def render_trade_row_card(card):
    # Render card with cost in yellow
    string = f"{render_card(card)}[\033[1m\033[93m{card.cost}\033[0m]"
    return string


def render_trade_row(game):
    # Render the trade row
    string = "\033[1mTrade Row:\033[0m "
    already_showing_explorer = False
    for card in game.trade_row:
        # Only show a single explorer
        if card.name == "Explorer" and already_showing_explorer:
            continue
        else:
            already_showing_explorer = True
        string += render_trade_row_card(card) + "\n"
    return string


def render_hand(player):
    string = "\033[1mHand   :\033[0m "
    for card in player.hand:
        string += render_card(card) + ", "
    return string

def render_play_area(player):
    string = "\033[1mPlay   :\033[0m "
    for card in player.play_area:
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
    # Show the cards in the players hand
    string += render_hand(player)
    string += "\n"
    string += render_play_area(player)

    return string


def render_action(action):
    # Render name of action class
    string = f"\033[1m\033[97m{action.__class__.__name__}\033[0m"
    # Render card name if action has a card attribute
    if hasattr(action, "card"):
        string += f" {render_card(action.card)}"
    
    # If this is a buy action render the cost 
    if action.__class__.__name__ == "BuyCard":
        string += f" for \033[1m\033[93m{action.card.cost}\033[0m trade"

    # Render the traderow card that will be scrapped as well as the card
    # responsible for this action
    if action.__class__.__name__ == "PlayCardScrapTraderow":
        string += f" scrapping {render_card(action.traderow_card)} using {render_card(action.action.card)}"


    return string


def render_actions_with_keys(key_action_map):
    # Render the actions in a numbered listn
    string = ""

    already_showing_explorer = False
    for key, action in key_action_map.items():
        # Only show a single explorer action 
        if action.__class__.__name__ == "BuyCard" and action.card.name == "Explorer":
            if already_showing_explorer:
                continue
            else:
                already_showing_explorer = True

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
