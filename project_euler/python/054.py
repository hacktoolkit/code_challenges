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
from collections import defaultdict

from utils import *


class PokerHandTypes(object):
    ROYAL_FLUSH = 0x900000
    STRAIGHT_FLUSH = 0x800000
    FOUR_OF_A_KIND = 0x700000
    FULL_HOUSE = 0x600000
    FLUSH = 0x500000
    STRAIGHT = 0x400000
    THREE_OF_A_KIND = 0x300000
    TWO_PAIRS = 0x200000
    ONE_PAIR = 0x100000
    HIGH_CARD = 0x0


class PokerHand(object):
    CARD_VALUES = {
        '2' : 2,
        '3' : 3,
        '4' : 4,
        '5' : 5,
        '6' : 6,
        '7' : 7,
        '8' : 8,
        '9' : 9,
        '10' : 10,
        'T' : 10,
        'J' : 11,
        'Q' : 12,
        'K' : 13,
        'A' : 14,
    }

    def __init__(self, cards):
        assert(len(cards) == 5)

        self.cards = cards

        self.suits = self.get_suits()
        self.ranks, self.ranks_scores = self.get_ranks_with_scores()

        self.rank_counts = defaultdict(int)
        for rank in self.ranks:
            self.rank_counts[rank] += 1
        self.sorted_rank_counts = sorted(self.rank_counts.items(), key=lambda (rank, count,): 100 * count + PokerHand.CARD_VALUES[rank], reverse=True)

        self.hex_score = ''.join([hex(rank_score)[2:] for rank_score in self.ranks_scores])
        self.grouped_hex_score = ''.join([hex(PokerHand.CARD_VALUES[rank])[2:] for (rank, count,) in self.sorted_rank_counts])

        self.hand_type = self.get_hand_type()

        self.score = self.get_score()

    def get_suits(self):
        suits = [card[1] for card in self.cards]
        return suits

    def get_ranks_with_scores(self):
        ranks = [card[0] for card in self.cards]
        ranks_scores = sorted([PokerHand.CARD_VALUES[rank] for rank in ranks], reverse=True)

        return ranks, ranks_scores

    def get_hand_type(self):
        hand_type = None

        if self.is_royal_flush():
            hand_type = PokerHandTypes.ROYAL_FLUSH
        elif self.is_straight_flush():
            hand_type = PokerHandTypes.STRAIGHT_FLUSH
        elif self.is_four_of_kind():
            hand_type = PokerHandTypes.FOUR_OF_A_KIND
        elif self.is_full_house():
            hand_type = PokerHandTypes.FULL_HOUSE
        elif self.is_flush():
            hand_type = PokerHandTypes.FLUSH
        elif self.is_straight():
            hand_type = PokerHandTypes.STRAIGHT
        elif self.is_three_of_kind():
            hand_type = PokerHandTypes.THREE_OF_A_KIND
        elif self.is_two_pairs():
            hand_type = PokerHandTypes.TWO_PAIRS
        elif self.is_one_pair():
            hand_type = PokerHandTypes.ONE_PAIR
        elif self.is_high_card():
            hand_type = PokerHandTypes.HIGH_CARD
        else:
            # impossible case
            pass

        return hand_type

    def get_score(self):
        """Gets a raw score based on the hand
        https://en.wikipedia.org/wiki/List_of_poker_hands
        """
        score = 0

        hand_type = self.hand_type
        base_score = hand_type  # (0x900000 for ROYAL_FLUSH down to 0x100000 for ONE PAIR and 0x0 for HIGH_CARD)
        grouped_hex_score_int = int('0x' + self.grouped_hex_score, 0)

        scoring_methods = {
            PokerHandTypes.ROYAL_FLUSH : lambda: base_score,
            PokerHandTypes.STRAIGHT_FLUSH : lambda: base_score + int( hex(self.ranks_scores[1] if self._is_a5_straight else self.ranks_scores[0]), 0),
            PokerHandTypes.FOUR_OF_A_KIND : lambda: base_score + int(hex(PokerHand.CARD_VALUES[self.sorted_rank_counts[0][0]]), 0),
            PokerHandTypes.FULL_HOUSE : lambda: base_score + int(hex(PokerHand.CARD_VALUES[self.sorted_rank_counts[0][0]]), 0),
            PokerHandTypes.FLUSH : lambda: base_score + int('0x' + self.hex_score, 0),
            PokerHandTypes.STRAIGHT : lambda: base_score + int(hex(self.ranks_scores[1] if self._is_a5_straight else self.ranks_scores[0]), 0),
            PokerHandTypes.THREE_OF_A_KIND : lambda: base_score + grouped_hex_score_int,
            PokerHandTypes.TWO_PAIRS : lambda: base_score + grouped_hex_score_int,
            PokerHandTypes.ONE_PAIR : lambda: base_score + grouped_hex_score_int,
            # 0xfffff = 1048575, so starting one pair at 2M is fine
            PokerHandTypes.HIGH_CARD : lambda: base_score + int('0x' + self.hex_score, 0),
        }

        scoring_method = scoring_methods[hand_type]
        score = scoring_method()

        return score

    def is_royal_flush(self):
        result = self.is_straight_flush() and self.ranks_scores[0] == PokerHand.CARD_VALUES['A']
        return result

    def is_strictly_straight_flush(self):
        result = self.is_straight_flush and self.ranks_scores[0] < PokerHand.CARD_VALUES['A']
        return result

    def is_straight_flush(self):
        result = self.is_flush() and self.is_straight()
        return result


    def is_four_of_kind(self):
        result = (
            self.sorted_rank_counts[0][1] == 4
            and self.sorted_rank_counts[1][1] == 1
        )
        return result

    def is_full_house(self):
        result = (
            len(set(self.ranks)) == 2
            and (
                self.sorted_rank_counts[0][1] == 3
                and self.sorted_rank_counts[1][1] == 2
            )
        )
        return result

    def is_flush(self):
        result = len(set(self.suits)) == 1
        return result

    def is_straight(self):
        result = self.is_regular_straight() or self.is_a5_straight()
        return result

    def is_regular_straight(self):
        self._is_a5_straight = False
        result = len(set(self.ranks_scores)) == 5 and self.ranks_scores[0] - 4 == self.ranks_scores[-1]
        return result

    def is_a5_straight(self):
        self._is_a5_straight = True
        result = (
            len(set(self.ranks_scores)) == 5
            and self.ranks_scores[0] == PokerHand.CARD_VALUES['A']
            and self.ranks_scores[1:] == [2, 3, 4, 5,]
        )
        return result

    def is_three_of_kind(self):
        result = (
            self.sorted_rank_counts[0][1] == 3
            and self.sorted_rank_counts[1][1] == 1
            and self.sorted_rank_counts[2][1] == 1
        )
        return result

    def is_two_pairs(self):
        result = (
            self.sorted_rank_counts[0][1] == 2
            and self.sorted_rank_counts[1][1] == 2
            and self.sorted_rank_counts[2][1] == 1
        )
        return result

    def is_one_pair(self):
        result = self.sorted_rank_counts[0][1] == 2 and self.sorted_rank_counts[1][1] == 1
        return result

    def is_high_card(self):
        result = len(set(self.ranks_scores)) == 5 and self.sorted_rank_counts[0][1] == 1
        return result


class Solution(object):
    EXPECTED_ANSWER = 376

    def __init__(self):
        pass
    
    def solve(self):
        poker_hands = self.get_poker_hands()

        p1_wins = 0
        p2_wins = 0
        for (hand1, hand2,) in poker_hands:
            winner = self.get_poker_hand_winner(hand1, hand2)
            debug_hand_types = (
                # PokerHandTypes.ROYAL_FLUSH,
                # PokerHandTypes.STRAIGHT_FLUSH,
                # PokerHandTypes.FOUR_OF_A_KIND,
                # PokerHandTypes.FULL_HOUSE,
                # PokerHandTypes.FLUSH,
                # PokerHandTypes.STRAIGHT,
                # PokerHandTypes.THREE_OF_A_KIND,
                # PokerHandTypes.TWO_PAIRS,
                # PokerHandTypes.ONE_PAIR,
                # PokerHandTypes.HIGH_CARD,
             )
            if hand1.hand_type in debug_hand_types and hand2.hand_type in debug_hand_types:
                print hand1.cards, hand1.hand_type, hand1.score, hand1.hex_score, hand2.cards, hand2.hand_type, hand2.score, hand2.hex_score, winner
            if winner == 1:
                p1_wins += 1
            elif winner == 2:
                p2_wins += 1
            else:
                # do nothing if tie
                pass

        answer = p1_wins
        return answer


    def get_poker_hands(self):
        poker_hands_file = 'p054_poker.txt'
        f = open(poker_hands_file, 'r')
        lines = f.readlines()
        poker_hands = []
        for line in lines:
            cards = line.strip().split(' ')
            assert(len(cards) == 10)
            hand1 = PokerHand(cards[:5])
            hand2 = PokerHand(cards[-5:])
            poker_hands.append((hand1, hand2,))
        f.close()
        return poker_hands

    def get_poker_hand_winner(self, hand1, hand2):
        if hand1.score > hand2.score:
            winner = 1
        elif hand2.score > hand1.score:
            winner = 2
        else:
            winner = 0

        return winner


def main():
    solution = Solution()
    answer = solution.solve()

    print 'Expected: %s, Answer: %s' % (Solution.EXPECTED_ANSWER, answer)


if __name__ == '__main__':
    main()
