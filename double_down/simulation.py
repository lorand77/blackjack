import random

ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
rank_values = {"2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":10, "Q":10, "K":10}
suits = ["♡", "♢", "♠", "♣"]

NUMBER_OF_DECKS = 1

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

def has_ace(hand):
    for card in hand:
        if card[0] == "A":
            return True
    return False

def hand_value_without_one_ace(hand):
    v = 0
    for card in hand:
        if card[0] != "A":
            v += rank_values[card[0]]
    n_aces = 0       
    for card in hand:
        if card[0] == "A":
            n_aces += 1
    if n_aces<1:
        raise("hand should have an Ace")
    v += n_aces-1
    return v

def game_round():
    global chips

    bet = 1

    deck = []
    for r in ranks:
        for s in suits:
            deck.append((r, s))
    deck = deck * NUMBER_OF_DECKS
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

    if hand_value(player_hand) == 11 or (hand_value(player_hand) == 10 and
                     hand_value(dealer_hand) < 10) or (hand_value(player_hand) == 9 and hand_value(dealer_hand) > 2 and
                     hand_value(dealer_hand) < 7) or (has_ace(player_hand) and hand_value_without_one_ace(player_hand) < 9 and
                     ((hand_value(dealer_hand) == 2 and hand_value_without_one_ace(player_hand) == 7) or (hand_value(dealer_hand) == 3 and
                     hand_value_without_one_ace(player_hand) <= 7 and hand_value_without_one_ace(player_hand) >= 6) or (hand_value(dealer_hand) == 4 and
                     hand_value_without_one_ace(player_hand) <= 7 and hand_value_without_one_ace(player_hand) >= 4) or (hand_value(dealer_hand) == 5 and
                     hand_value_without_one_ace(player_hand) <= 7 and hand_value_without_one_ace(player_hand) >= 2) or (hand_value(dealer_hand) == 6))):
        bet = 2
        player_hand.append(deal_card(deck))
    else:
        while True:
            if has_ace(player_hand) and hand_value_without_one_ace(player_hand) < 10:
                if hand_value_without_one_ace(player_hand) > 7 or (hand_value_without_one_ace(player_hand) == 7 and hand_value(dealer_hand) < 9):
                    break
            else:
                if hand_value(player_hand) >= 17 or ((hand_value(player_hand) >= 12 and hand_value(dealer_hand) < 7) and 
                                                not (hand_value(player_hand) == 12 and hand_value(dealer_hand) <= 3)):
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
    

counts = {"player_wins_bj" : 0, "draw_bj" : 0,"player_busted" : 0, "dealer_busted" : 0, 
    "dealer_wins_bj" : 0, "player_wins" : 0, "dealer_wins" : 0, "draw" : 0}
chips = 0
for i in range(1000000):
    game_round()
print(counts)
print(chips)