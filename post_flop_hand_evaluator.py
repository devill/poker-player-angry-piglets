
class PostFlopHandEvaluator:
    def __init__(self, community_cards, hole_cards):
        self.community_cards = community_cards
        self.hole_cards = hole_cards

    def has_three_of_a_kind_with_two_cards_in_hand(self):
        if not self.has_pair_in_hand():
            return False

        if self.n_of_a_kind_with_card_in_hand(0) > 0:
            return True

        return False

    def has_pair_in_hand(self):
        return self.hole_cards[0]['rank'] ==  self.hole_cards[1]['rank']

    def n_of_a_kind_with_card_in_hand(self, index):
        count = 0
        for card in self.community_cards:
            if card['rank'] == self.hole_cards[index]['rank']:
                count +=1

        return count



