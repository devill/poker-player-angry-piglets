from post_flop_hand_evaluator import PostFlopHandEvaluator
from config import Config
import logging
import sys
import traceback

log = logging.getLogger('player.Player')
log.addHandler(logging.StreamHandler(sys.stderr))
log.setLevel(logging.DEBUG)


class Player:
    VERSION_FORMAT = "AngryPiglet [config: {config}]"
    VERSION = "Default Python folding player"

    def __init__(self):
        self.config = Config.get_instance()
        self.VERSION = self.VERSION_FORMAT.format(config=self.config.version)

    def betRequest(self, game_state):
        try:
            log.info('config version: %s', self.config.version)
            self.player = self.get_our_player(game_state)
            self.get_our_hand()
            chen_score = self.chen_formula()
            chen_score_treshold = int(self.config.heads_up_threshold)

            if len(game_state["community_cards"]) > 0:
                helper = PostFlopHandEvaluator(game_state["community_cards"], self.player["hole_cards"])
                if self.config.check_three_of_a_kind:
                    if helper.has_three_of_a_kind_with_two_cards_in_hand():
                        log.info('three of a kind with two cards in hand')
                        if game_state["current_buy_in"] < 200:
                            return 200
                        else:
                            return 10000
                    if helper.has_three_of_a_kind_with_one_card_in_hand():
                        log.info('three of a kind with one card in hand')
                        if game_state["current_buy_in"] < 200:
                            return 200
                        else:
                            return 10000
                if self.config.check_two_pairs:
                    if helper.has_two_pairs_with_one_card_from_both_in_hand():
                        log.info('two pairs with one card from both in hand')
                        if game_state["current_buy_in"] < 200:
                            return 200
                        else:
                            return int(self.config.two_pair_bet)

            if self.active_players(game_state) > 2:
                chen_score_treshold = int(self.config.default_threshold)
            if chen_score >= chen_score_treshold:
                return 10000
            else:
                if self.get_position(game_state) == 2 and self.no_raise(game_state) and len(game_state["community_cards"]) == 0:
                    if self.active_players(game_state) > 3:
                        return game_state["current_buy_in"] - self.player["bet"] + game_state["minimum_raise"]
                    else:
                        return game_state["small_blind"] * 2
                if self.get_position(game_state) == 1 and self.no_raise(game_state) and len(game_state["community_cards"]) == 0:
                    if self.active_players(game_state) > 3:
                        return game_state["current_buy_in"] - self.player["bet"] + game_state["minimum_raise"]
                    else:
                        return game_state["small_blind"] * 2
                if self.min_raise_happened(game_state) and chen_score > int(self.config.aggression_index):
                    return game_state["current_buy_in"] - self.player["bet"] + (game_state["minimum_raise"] * 2)
                if game_state["current_buy_in"] <= self.player["bet"] * 2 and chen_score > int(self.config.safety_index):
                    return game_state["current_buy_in"]
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
        self.hole_cards_ranks = "".join([self.convert_to_char(card["rank"]) for card in self.hole_cards])
        self.hole_cards_suits = "".join([card["suit"][0] for card in self.hole_cards])

    def have_pair(self):
        return self.hole_cards[0]["rank"] == self.hole_cards[1]["rank"]

    def is_suited(self):
        return self.hole_cards[0]["suit"] == self.hole_cards[1]["suit"]

    def have_rank(self, rank):
        return rank in self.hole_cards_ranks

    def convert_to_char(self, rank):
        if rank == "10":
            return "T"
        return rank

    def chen_formula(self):
        score = self.score_of_highest_card()
        if self.have_pair():
            score *= 2
        if self.is_suited():
            score += 2
        gap_size = self.gap_size(self.hole_cards_ranks[0], self.hole_cards_ranks[1])
        gap_size_to_points = {
            0: 0,
            1: 1,
            2: 2,
            3: 4,
        }
        score -= gap_size_to_points.get(gap_size, 5)
        if gap_size < 2 and not(self.have_rank("A") or self.have_rank("K") or self.have_rank("Q")):
            score += 1
        return round(score)



    def score_of_highest_card(self):
        if self.have_rank("A"):
            return 10
        elif self.have_rank("K"):
            return 8
        elif self.have_rank("Q"):
            return 7
        elif self.have_rank("J"):
            return 6
        elif self.have_rank("T"):
            return 5
        else:
            return int(sorted(self.hole_cards_ranks)[-1])/2.0

    def gap_size(self, card1, card2):
        ranks = "23456789TJQKA"
        return max(0, abs(ranks.find(card1) - ranks.find(card2))-1)

    def active_players(self, game_state):
        count = 0
        for player in game_state["players"]:
            if player["status"] != "out":
                count += 1
        return count

    def is_big_blind(self, game_state):
        return (game_state["dealer"]+2)%(len(game_state["players"])) == game_state["in_action"]

    def no_raise(self, game_state):
        return game_state["small_blind"] * 2 == game_state["current_buy_in"]

    def get_position(self, game_state):
        if (game_state["dealer"])%(len(game_state["players"])) == game_state["in_action"]:
            return 0
        if (game_state["dealer"]+1)%(len(game_state["players"])) == game_state["in_action"]:
            return 1
        if (game_state["dealer"]+2)%(len(game_state["players"])) == game_state["in_action"]:
            return 2
        else:
            return 9

    def min_raise_happened(self, game_state):
        return game_state["current_buy_in"] <= game_state["small_blind"] * 4
