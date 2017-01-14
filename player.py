import traceback


class Player:
    VERSION = "Default Python folding player"

    def betRequest(self, game_state):
        try:
            self.player = self.get_our_player(game_state)
            self.get_our_hand()
            if self.have_pair():
                return 10000
            if self.is_suited() and ((self.have_rank("A") and self.have_rank("K")) or (self.have_rank("K") and self.have_rank("Q"))):
                return 10000
            return 0
        except:
            traceback.print_exc()
            return 10000

    def showdown(self, game_state):
        pass

    def get_our_player(self, game_state):
        return game_state["players"][game_state["in_action"]]

    def get_our_hand(self):
        self.hole_cards = self.player["hole_cards"]
        self.hole_cards_ranks = "".join([card["rank"] for card in self.hole_cards])
        self.hole_cards_suits = "".join([card["suit"][0] for card in self.hole_cards])

    def have_pair(self):
        return self.hole_cards[0]["rank"] == self.hole_cards[1]["rank"]

    def is_suited(self):
        return self.hole_cards[0]["suit"] == self.hole_cards[1]["suit"]

    def have_rank(self, rank):
        return rank in self.hole_cards_ranks
