
preprompt = """
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

card_info_prompt = "Here are details and stratedgy for every card in the game:\n"
card_info_prompt += """
Card: Explorer 
How to Play:
When you play Explorer, gain 2 Trade. At any time, you may scrap Explorer to gain 2 Combat.
Explorers are not shuffled into the main Trade deck. They are kept in a separate pile face up next to the Trade Row (opposite the Trade deck) where they are always available to be acquired.
When an Explorer is scrapped, it is placed back on top of the Explorer pile, not the scrap heap like other cards.
Strategy:
Explorers are a basic utility card always available to give your starting deck a trade boost, assuming there is nothing more cost effective in the Trade row. One important skill in the game is learning when mid game to stop buying Explorers and start scrapping them for the Combat bonus and to improve the efficiency of your deck.
"""
card_info_prompt += """
Card: Scout 
How to Play:
When you play Scout, gain 1 Trade.
Strategy
Scouts are one of the two different cards each player has in their starting deck. One of the most crucial strategies in the game is scrapping the starter cards out of your deck to increase deck efficiency (i.e. increasing the odds of drawing other more powerful cards). It is a matter of personal preference (and some lively debate) whether it is best to scrap Vipers or Scouts first, but nevertheless the player who scraps starters the fastest is most often the winner.
"""
card_info_prompt += """
Card: Viper 
How to Play:
When you play Viper, gain 1 Combat.
Strategy:
Vipers are one of the two different cards each player has in their starting deck. One of the most crucial strategies in the game is scrapping the starter cards out of your deck to increase deck efficiency (i.e. increasing the odds of drawing other more powerful cards). It is a matter of personal preference (and some lively debate) whether it is best to scrap Vipers or Scouts first, but nevertheless the player who scraps starters the fastest is most often the winner.
"""
card_info_prompt += """
Card: Blob Fighter 
How to play:
When you play Blob Fighter, gain 3 Combat. At any time, if you have another Blob card in play, you may draw a card.
Strategy:
At one cost and 3 combat, Blob Fighter has the typical strong Blob combat value per trade cost. However the Blob Fighter really shines in a Blob-heavy deck when it can consistently trigger the draw and other Blob card's ally ability.
"""
card_info_prompt += """
Card: Trade Pod 
How to Play:
When you play Trade Pod, gain 3 Trade. At any time, if you have a Blob card in play you may gain 2 Combat.
Strategy:
Two cost for three trade is a great deal that is very hard to pass up, especially in the first few turns of the game. As the game progresses, the value of the Trade Pod goes down, unless paired with haulers.
"""
card_info_prompt += """
Card: Battle Pod 
How to Play:
When you play Battle Pod, gain 4 Combat and scrap one of the cards currently in the Trade Row. At any time, if you have another Blob card in play, you may gain 2 Combat.
Strategy:
The Battle Pod is a powerful "little" ship at 2 cost and 6 potential damage - great to counter an opponent's base in the early game.
However its real strength is in its ability to help control the trade row. Keep a close eye on what your opponent is buying and use the Battle Pod to keep strong combos away from him. If you know your opponent has a lot of trade, then it's probably good to clear the most powerful cards off the trade row. Also, if there is not a good option in the Trade Row for you to purchase, Battle Pod can help flip a better card for you to buy.
But be careful, sometimes you can flip an even better card for your opponent. Scrap with care!
"""
card_info_prompt += """
Card: Ram 
How to Play:
When you play Ram, gain 5 Combat. At any time, if you have another Blob card in play, you may gain 2 Combat. Also, at any time you may scrap Ram to gain 3 Trade.
Strategy:
A typically powerful ship for the Blob faction, the Ram is great as an early buy. The Ram provides a lethal dose of damage and is often scrapped in the early game to purchase a more powerful card.
"""
card_info_prompt += """
Card: Blob Destroyer 
How to Play:
When you play Blob Destroyer, gain 6 Combat. At any time, if you have another Blob card in play, you may choose to: destroy any base in play, or scrap a card in the trade row, or both.
Strategy:
With its 6 Combat for 4 cost, the Blob Destroyer makes a great early game buy for an "aggro" deck building strategy. When paired with other Blob cards, the Destroyer lives up to its name. It is an essential card when your opponent is playing a base strategy due to its ability to remove bases both with its ally ability and solid 6 Combat.
"""
card_info_prompt += """
Card: Battle Blob 
How to Play:
When you play Battle Blob, gain 8 Combat. At any time, if you have another Blob card in play, you may draw a card. At any time, you may scrap Battle Blob to gain 4 Combat.Note: In the digital app, the ally ability is automatic and mandatory. However when playing with physical cards the ally ability is optional.
Strategy:
Battle Blob is a rather straightforward powerhouse card.  The 8 Combat and a possible draw alone makes the card well worth the 6 Trade cost in virtually any deck.  Where the true strategy comes in with Battle Blob is the scrap ability.  Normally the scrap is used in the end game either in the final turn, or when it is relatively certain given the number of cards remaining in your deck that you will not get a chance to play Battle Blob again.  Otherwise it is rarely scrapped during the mid game.
"""
card_info_prompt += """
Card: Blob Carrier 
How to Play:
When you play Blob Carrier, gain 7 Combat. At any time, if you have another Blob card in play, you may acquire any ship without paying its cost and place it on top of your deck.
Strategy:
Typically strong 7 Combat as a Blob ship, this ship is usually a worthy buy at six cost, even if you're not likely to use it's ally ability. However it's ally ability is it's true strength. The ability to get any ship for free AND place it atop your deck (perhaps even play it the same turn with a draw ability) is incredibly powerful when you can trigger it consistently. Blob Carrier pairs well with any Blob card, Mech World, and Stealth Needle.
"""
card_info_prompt += """
Card: Mothership
How to Play:
When you play Mothership, gain 6 Combat and draw a card. At any time, if you have another Blob card in play, draw a card.
Strategy:
A rather simple, no-frills yet powerful card. If you can afford it, 7-cost for a 6 Combat card that replaces itself is a good deal - it certainly doesn't hurt. The extra draw as an ally ability is a nice bonus, and makes Mothership one of the rare cards capable of drawing two cards consistently.
"""
card_info_prompt += """
Card: Blob Wheel
How to Play: 
When you play Blob Wheel, gain 1 Combat. At any time you can scrap the card in exchange of 3 trade. With a base strength of 5 it will probably ignored if other bases are in play.
Strategy:
With a cost of 3 its a cheap way to put up a base up with decent defense. Adding 1 combat aint powerful. Most of time it will be used as a investment for more expensive buys in later turns.
"""
card_info_prompt += """
Card: Hive
How to Play:
When you play The Hive you get 3 Combat. Its a base with strength of 5. The ally ability lets you draw another card.
Strategy: 
With a cost of 5 trade a good investment to bring some combat to your game and if the ally ability triggers its prolonging your turn.
"""
card_info_prompt += """
Card: Blob World 
How to Play: 
When you play Blob World you get the choice between an attack of 5 combat or drawing cards equel to the many blob cards you played this turn.
Strategy: 
This can be a great card if you have a lot Blob cards in your deck. It can really catalyst your turn and potentialy building up a large combat attack that can finish your opponent with a swift blow. Because of that chance it is easy to explain why this card cost 8 trade.
"""
