import random

ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
suites = ["♡", "♢", "♠", "♣"]
deck = []

for r in ranks:
    for s in suites:
        deck.append((r, s))

def print_deck(deck):
    for card in deck:
        print(card[0]+card[1], end=" ")
    print()

print_deck(deck)

random.shuffle(deck)
print_deck(deck)