import random
import matplotlib.pyplot as plt

ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
rank_values = {"2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":10, "Q":10, "K":10}
suits = ["♡", "♢", "♠", "♣"]

NUMBER_OF_DECKS = 6
count_history = [0]

def deal_card(deck):
    return deck.pop(0)

deck = []
for r in ranks:
    for s in suits:
        deck.append((r, s))
deck = deck * NUMBER_OF_DECKS
random.shuffle(deck)

for card in deck:
    if card[0] == "A" or rank_values[card[0]] > 9:
        count_history.append(count_history[-1] -1)
    elif rank_values[card[0]] < 7:
        count_history.append(count_history[-1] +1)
    else:
        count_history.append(count_history[-1])

x = list(range(0,52*NUMBER_OF_DECKS+1))
for i in range(0,len(x)):
    x[i] /= 52
#plt.plot(x,count_history)
#plt.show()

true_count_history = []
for i in range(0,52*NUMBER_OF_DECKS+1):
    true_count_history.append(count_history[i]/((52*NUMBER_OF_DECKS-i)//52+1))
    #true_count_history.append((52*NUMBER_OF_DECKS-i)//52+1)

plt.plot(x[:int(52*NUMBER_OF_DECKS*0.75)],true_count_history[:int(52*NUMBER_OF_DECKS*0.75)])
plt.show()    