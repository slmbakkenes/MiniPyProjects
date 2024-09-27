import random

# Card categories and values
card_categories = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
cards_list = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
deck = [(card, category) for category in card_categories for card in cards_list]

# Shuffle deck
random.shuffle(deck)


# Card value calculation
def card_value(card):
    if card[0] in ['Jack', 'Queen', 'King']:
        return 10
    elif card[0] == 'Ace':
        return 11
    else:
        return int(card[0])


# Adjust for Ace when score exceeds 21
def adjust_for_ace(cards, score):
    aces = sum(1 for card in cards if card[0] == 'Ace')
    while score > 21 and aces:
        score -= 10
        aces -= 1
    return score


# Display cards
def display_cards(player, cards):
    print(f"Cards {player} Has: {cards}")


# Betting system
def get_bet(balance):
    while True:
        try:
            bet = int(input(f"Your balance is {balance}. How much would you like to bet? "))
            if bet > balance:
                print("You cannot bet more than your balance.")
            else:
                return bet
        except ValueError:
            print("Please enter a valid number.")


# Main game loop
balance = 100  # Starting balance for the player

while balance > 0:
    # Deal cards
    player_card = [deck.pop(), deck.pop()]
    dealer_card = [deck.pop(), deck.pop()]

    # Get bet from player
    bet = get_bet(balance)

    # Calculate initial scores
    player_score = sum(card_value(card) for card in player_card)
    dealer_score = sum(card_value(card) for card in dealer_card)

    # Check for initial Blackjack
    player_score = adjust_for_ace(player_card, player_score)
    dealer_score = adjust_for_ace(dealer_card, dealer_score)

    # Show cards
    display_cards("Player", player_card)
    print(f"Score Of The Player: {player_score}")
    print("\n")

    # Check if player has a Blackjack
    if player_score == 21:
        print("Blackjack! Player wins!")
        balance += bet
        continue

    # Player turn
    while True:
        choice = input('What do you want? ["hit" to request another card, "stand" to stop]: ').lower()
        if choice == "play":
            new_card = deck.pop()
            player_card.append(new_card)
            player_score = sum(card_value(card) for card in player_card)
            player_score = adjust_for_ace(player_card, player_score)
            display_cards("Player", player_card)
            print(f"Score Of The Player: {player_score}")
            if player_score > 21:
                print("Player busts! Dealer wins.")
                balance -= bet
                break
        elif choice == "stop":
            break
        else:
            print("Invalid choice. Please try again.")

    # If player busts, end the round
    if player_score > 21:
        continue

    # Dealer turn
    print("\nDealer's Turn:")
    display_cards("Dealer", dealer_card)
    print(f"Score Of The Dealer: {dealer_score}")

    while dealer_score < 17:
        new_card = deck.pop()
        dealer_card.append(new_card)
        dealer_score = sum(card_value(card) for card in dealer_card)
        dealer_score = adjust_for_ace(dealer_card, dealer_score)
        display_cards("Dealer", dealer_card)
        print(f"Score Of The Dealer: {dealer_score}")

    # Determine winner
    if dealer_score > 21:
        print("Dealer busts! Player wins.")
        balance += bet
    elif player_score > dealer_score:
        print("Player wins! Higher score than Dealer.")
        balance += bet
    elif dealer_score > player_score:
        print("Dealer wins! Higher score than Player.")
        balance -= bet
    else:
        print("It's a tie. No one wins.")

    # Check if the deck needs reshuffling
    if len(deck) < 10:
        print("Reshuffling deck...")
        deck = [(card, category) for category in card_categories for card in cards_list]
        random.shuffle(deck)

# Game over
print("Game over. You have run out of balance.")
