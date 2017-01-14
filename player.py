
class Player:
    VERSION = "Default Python folding player"

    def betRequest(self, game_state):
        try:
            self.player = self.get_our_player(game_state)
            self.hole_cards = self.get_our_hand()
            if self.have_pair():
                return 10000
            return 0
        except:
            return 10000

    def showdown(self, game_state):
        pass

    def get_our_player(self, game_state):
        for player in game_state["players"]:
            if player["name"] == "Angry Piglets":
                return player
        0/0

    def get_our_hand(self):
        self.hole_cards = self.player["hole_cards"]
        self.hole_cards_ranks = None

    def have_pair(self):
        return self.hole_cards[0]["rank"] == self.hole_cards[1]["rank"]

    def is_suited(self):
        return self.hole_cards[0]["suit"] == self.hole_cards[1]["suit"]

    def have_ace(self):
        return self.hole_cards[0]["suit"] == "A" or self.hole_cards[1]["suit"] == "A"
