import random

ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
rank_values = {"2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":10, "Q":10, "K":10}
suits = ["♡", "♢", "♠", "♣"]

bet = 1

def print_cards(cards):
    for card in cards:
        print(card[0]+card[1], end=" ")
    print("\tValue:",hand_value(cards))    

def deal_card(deck):
    return deck.pop(0)

def hand_value(hand):
    v = 0
    for card in hand:
        if card[0] != "A":
            v += rank_values[card[0]]
    n_aces = 0       
    for card in hand:
        if card[0] == "A":
            n_aces += 1
    if n_aces == 0:
        return v
    elif n_aces == 1:
        if v+11 <= 21:
            return v+11
        else:
            return v+1
    else:
        v += n_aces-1
        if v+11 <= 21:
            return v+11
        else:
            return v+1

def is_blackjack(hand):
    return len(hand) == 2 and hand_value(hand) == 21

def game_round():
    global chips

    deck = []
    for r in ranks:
        for s in suits:
            deck.append((r, s))
    random.shuffle(deck)

    dealer_hand = []
    player_hand = []

    dealer_hand.append(deal_card(deck))
    player_hand.append(deal_card(deck))
    player_hand.append(deal_card(deck))

    if is_blackjack(player_hand):
        dealer_hand.append(deal_card(deck))
        if not is_blackjack(dealer_hand):
            chips += bet * 3 / 2
            counts["player_wins_bj"] += 1
        else:
            counts["draw_bj"] += 1
        return
    
    while True:
        if hand_value(player_hand) >= limit:
            break
        player_hand.append(deal_card(deck))
        if hand_value(player_hand) >= 21:
            break
    
    if hand_value(player_hand) > 21:
        chips -= bet
        counts["player_busted"] += 1
        return
    
    while hand_value(dealer_hand) < 17:
        dealer_hand.append(deal_card(deck))

    if hand_value(dealer_hand) > 21:
        chips += bet
        counts["dealer_busted"] += 1
        return

    if is_blackjack(dealer_hand):
        chips -= bet
        counts["dealer_wins_bj"] += 1
        return

    if hand_value(player_hand) > hand_value(dealer_hand):
        chips += bet
        counts["player_wins"] += 1
    elif hand_value(player_hand) < hand_value(dealer_hand):
        chips -= bet
        counts["dealer_wins"] += 1
    else:
        counts["draw"] += 1
    
for limit in [12,13,14,15,16,17,18,19]:
    counts = {"player_wins_bj" : 0, "draw_bj" : 0,"player_busted" : 0, "dealer_busted" : 0, 
          "dealer_wins_bj" : 0, "player_wins" : 0, "dealer_wins" : 0, "draw" : 0}
    chips = 0
    for i in range(1000000):
        game_round()
    print(limit)
    print(counts)
    print(chips)
    print("--------------------------------------------------------------------")
