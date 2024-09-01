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

    deck = []
    for r in ranks:
        for s in suits:
            deck.append((r, s))
    deck = deck * NUMBER_OF_DECKS
    random.shuffle(deck)

    bets = [1]

    dealer_hand = []
    player_hands = [[]]

    dealer_hand.append(deal_card(deck))
    player_hands[0].append(deal_card(deck))
    player_hands[0].append(deal_card(deck))

    if is_blackjack(player_hands[0]):
        dealer_hand.append(deal_card(deck))
        if not is_blackjack(dealer_hand):
            chips += bets[0] * 3 / 2
            counts["player_wins_bj"] += 1
        else:
            counts["draw_bj"] += 1
        return

    if player_hands[0][0][0] == player_hands[0][1][0]:
        player_hands = [ [player_hands[0][0]], [player_hands[0][0]] ]
        player_hands[0].append(deal_card(deck))
        player_hands[1].append(deal_card(deck))
        counts["splits"] += 1

    bets = [1] * len(player_hands)

    for h in range(len(player_hands)):
        if hand_value(player_hands[h]) == 11 or (hand_value(player_hands[h]) == 10 and
                        hand_value(dealer_hand) < 10) or (hand_value(player_hands[h]) == 9 and hand_value(dealer_hand) > 2 and
                        hand_value(dealer_hand) < 7) or (has_ace(player_hands[h]) and hand_value_without_one_ace(player_hands[h]) < 9 and
                        ((hand_value(dealer_hand) == 2 and hand_value_without_one_ace(player_hands[h]) == 7) or (hand_value(dealer_hand) == 3 and
                        hand_value_without_one_ace(player_hands[h]) <= 7 and hand_value_without_one_ace(player_hands[h]) >= 6) or (hand_value(dealer_hand) == 4 and
                        hand_value_without_one_ace(player_hands[h]) <= 7 and hand_value_without_one_ace(player_hands[h]) >= 4) or (hand_value(dealer_hand) == 5 and
                        hand_value_without_one_ace(player_hands[h]) <= 7 and hand_value_without_one_ace(player_hands[h]) >= 2) or (hand_value(dealer_hand) == 6))):
            bets[h] = 2
            counts["double_down"] += 1
            player_hands[h].append(deal_card(deck))
        else:
            while True:
                if has_ace(player_hands[h]) and hand_value_without_one_ace(player_hands[h]) < 10:
                    if hand_value_without_one_ace(player_hands[h]) > 7 or (hand_value_without_one_ace(player_hands[h]) == 7 and hand_value(dealer_hand) < 9):
                        break
                else:
                    if hand_value(player_hands[h]) >= 17 or ((hand_value(player_hands[h]) >= 12 and hand_value(dealer_hand) < 7) and 
                                                    not (hand_value(player_hands[h]) == 12 and hand_value(dealer_hand) <= 3)):
                        break

                player_hands[h].append(deal_card(deck))
                if hand_value(player_hands[h]) >= 21:
                    break

    for h in range(len(player_hands)-1,-1,-1):    
        if hand_value(player_hands[h]) > 21:
            chips -= bets[h]
            counts["player_busted"] += 1
            del player_hands[h]
            del bets[h]
    if len(player_hands) == 0:
        return
    
    while hand_value(dealer_hand) < 17:
        dealer_hand.append(deal_card(deck))

    if hand_value(dealer_hand) > 21:
        for h in range(len(player_hands)):
            chips += bets[h]
        counts["dealer_busted"] += 1
        return

    if is_blackjack(dealer_hand):
        for h in range(len(player_hands)):
            chips -= bets[h]
        counts["dealer_wins_bj"] += 1
        return
   
    for h in range(len(player_hands)):
        if hand_value(player_hands[h]) > hand_value(dealer_hand):
            chips += bets[h]
            counts["player_wins"] += 1
        elif hand_value(player_hands[h]) < hand_value(dealer_hand):
            chips -= bets[h]
            counts["dealer_wins"] += 1
        else:
            counts["draw"] += 1
    

counts = {"player_wins_bj" : 0, "draw_bj" : 0,"player_busted" : 0, "dealer_busted" : 0, 
    "dealer_wins_bj" : 0, "player_wins" : 0, "dealer_wins" : 0, "draw" : 0, "double_down" : 0, "splits" : 0}
chips = 0
for i in range(1000000):
    game_round()
print(counts)
print(chips)