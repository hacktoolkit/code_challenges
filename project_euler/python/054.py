"""
http://projecteuler.net/problem=054

Poker hands

In the card game poker, a hand consists of five cards and are ranked, from lowest to highest, in the following way:

High Card: Highest value card.
One Pair: Two cards of the same value.
Two Pairs: Two different pairs.
Three of a Kind: Three cards of the same value.
Straight: All cards are consecutive values.
Flush: All cards of the same suit.
Full House: Three of a kind and a pair.
Four of a Kind: Four cards of the same value.
Straight Flush: All cards are consecutive values of same suit.
Royal Flush: Ten, Jack, Queen, King, Ace, in same suit.

The cards are valued in the order: 2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King, Ace.
If two players have the same ranked hands then the rank made up of the highest value wins; for example, a pair of eights beats a pair of fives (see example 1 below). But if two ranks tie, for example, both players have a pair of queens, then highest cards in each hand are compared (see example 4 below); if the highest cards tie then the next highest cards are compared, and so on.
Consider the following five hands dealt to two players:

Hand
Player 1
Player 2
Winner

1
5H 5C 6S 7S KD (Pair of Fives)
2C 3S 8S 8D TD (Pair of Eights)
Player 2

2
5D 8C 9S JS AC (Highest card Ace)
2C 5C 7D 8S QH (Highest card Queen)
Player 1

3
2D 9C AS AH AC (Three Aces)
3D 6D 7D TD QD (Flush  with Diamonds)
Player 2

4
4D 6S 9H QH QC (Pair of Queens Highest card Nine)
3D 6D 7H QD QS (Pair of Queens Highest card Seven)
Player 1

5
2H 2D 4C 4D 4S (Full House With Three Fours)
3C 3D 3S 9S 9D (Full House with Three Threes)
Player 1

The file, poker.txt, contains one-thousand random hands dealt to two players. Each line of the file contains ten cards (separated by a single space): the first five are Player 1's cards and the last five are Player 2's cards. You can assume that all hands are valid (no invalid characters or repeated cards), each player's hand is in no specific order, and in each hand there is a clear winner.

How many hands does Player 1 win?

Solution by jontsai <hello@jontsai.com>
"""
from utils import *

EXPECTED_ANSWER = 0

def get_poker_hands():
    poker_hands_file = 'p054_poker.txt'
    f = open(poker_hands_file, 'r')
    lines = f.readlines()
    poker_hands = []
    for line in lines:
        cards = line.strip().split(' ')
        assert(len(cards) == 10)
        hand1 = cards[:5]
        hand2 = cards[-5:]
        poker_hands.append((hand1, hand2,))
    f.close()
    return poker_hands

def get_poker_hand_winner(hand1, hand2):
    return 1

def solve():
    poker_hands = get_poker_hands()
    p1_wins = 0
    p2_wins = 0
    
    for (hand1, hand2,) in poker_hands:
        winner = get_poker_hand_winner(hand1, hand2)
        if winner == 1:
            p1_wins += 1
        else:
            p2_wins += 1
    answer = p1_wins
    return answer

def main():
    answer = solve()

    print 'Expected: %s, Answer: %s' % (EXPECTED_ANSWER, answer)

if __name__ == '__main__':
    main()
