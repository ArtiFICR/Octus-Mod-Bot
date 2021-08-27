async def getBlackJackTotal(card_number, blackjack_count):
    #print(f'Card number drawn: {card_number}')
    if card_number == 'A':
        if blackjack_count <= 10:
            blackjack_count += 11
        else:
            blackjack_count += 1
    elif card_number == '2':
        blackjack_count += 2
    elif card_number == '3':
        blackjack_count += 3
    elif card_number == '4':
        blackjack_count += 4
    elif card_number == '5':
        blackjack_count += 5
    elif card_number == '6':
        blackjack_count += 6
    elif card_number == '7':
        blackjack_count += 7
    elif card_number == '8':
        blackjack_count += 8
    elif card_number == '9':
        blackjack_count += 9
    elif card_number == 'T' or card_number == 'J' or card_number == 'Q' or card_number == 'K':
        blackjack_count += 10

    return blackjack_count
