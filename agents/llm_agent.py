"""Starrealms agent functions"""
import openai

from starrealms.action import EndTurn
from agents.agent import Agent
from starrealms.card import CardFaction
from starrealms.interface import render, render_action
from agents.llm_prompts import preprompt, card_info_prompt

class GPTAgent(Agent):
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if openai.api_key is None:
            raise ValueError("OPENAI_API_KEY is not set")

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

        prompt = preprompt + "\n" + game_state_prompt + "\n" + action_prompt

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
                    {"role": "system", "content": preprompt},
                    {"role": "assistant", "content": card_info_prompt},
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
