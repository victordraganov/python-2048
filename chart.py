import json
from json import JSONDecodeError
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
        try:
            output_file = open(filename, 'w')
        except FileNotFoundError:
            output_file = open(filename, 'w+')
        output_file.truncate()
        json.dump(self.top_players, output_file)
        output_file.close()

    def load(self, filename):
        try:
            input_file = open(filename, 'r')
        except FileNotFoundError:
            input_file = open(filename, 'w+')

        try:
            self.top_players = json.load(input_file)
        except JSONDecodeError:
            self.top_players = {}
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