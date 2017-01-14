
class Player:
    VERSION = "Default Python folding player"

    def betRequest(self, game_state):
        return 10000
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
        return self.player["hole_cards"]

    def have_pair(self):
        return self.hole_cards[0]["rank"] == self.hole_cards[1]["rank"]
