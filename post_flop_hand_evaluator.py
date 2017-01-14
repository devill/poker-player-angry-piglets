
class PostFlopHandEvaluator:
    def __init__(self, community_cards, hole_cards):
        self.community_cards = community_cards
        self.hole_cards = hole_cards

    def has_three_of_a_kind_with_two_cards_in_hand(self):
        if not self.has_pair_in_hand():
            return False

        if self.nof_same_rank_community_card_as_hole_card(0) > 0:
            return True

        return False

    def has_three_of_a_kind_with_one_card_in_hand(self):
        if self.nof_same_rank_community_card_as_hole_card(0) > 1:
            return True

        if self.nof_same_rank_community_card_as_hole_card(1) > 1:
            return True

        return False

    def has_two_pairs_with_one_card_from_both_in_hand(self):
        if self.nof_same_rank_community_card_as_hole_card(0) > 0 and self.nof_same_rank_community_card_as_hole_card(1) > 0:
            return True

        return False

    def has_four_of_a_kind(self):
        if self.nof_same_rank_community_card_as_hole_card(0) >= 3 or self.nof_same_rank_community_card_as_hole_card(1) >= 3:
            return True

        if self.has_pair_in_hand():
            return self.nof_same_rank_community_card_as_hole_card(0) >= 2

        return False

    def has_pair_in_hand(self):
        return self.hole_cards[0]['rank'] ==  self.hole_cards[1]['rank']

    def nof_same_rank_community_card_as_hole_card(self, index):
        count = 0
        for card in self.community_cards:
            if card['rank'] == self.hole_cards[index]['rank']:
                count +=1

        return count

    # def has_two_pair_with_no_pair_on_board(self):
