import json
import constants


class Chart:

    def __init__(self):
        self.top_players = [('', 0)
                            for _ in range(constants.HIGH_SCORE_CHART_SIZE)]

    def __iter__(self):
        return iter(self.top_players)

    def is_top_score(self, score):
        return any(player for player in self.top_players if player[1] <= score)

    def save(self, filename):
        output_file = open(filename, 'w')
        output_file.truncate()
        json.dump(self.top_players, output_file)
        output_file.close()
# TODO

    def load(self, filename):
        input_file = open(filename, 'r')
        self.top_players = json.load(input_file)
        input_file.close()

    def add(self, name, score):
        if not self.is_top_score(score):
            return
        for player in enumerate(self.top_players):
            if player[1][1] <= score:
                self.top_players.insert(player[0], (name, score))
                break
        self.top_players.pop()

    def reset(self):
        self.top_players = [('', 0)
                            for _ in range(constants.HIGH_SCORE_CHART_SIZE)]