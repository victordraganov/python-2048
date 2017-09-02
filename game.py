from enum import Enum
from chart import Chart
from exceptions import GridWinScoreReachedException
import constants


class State(Enum):
    running = 'running'
    game_over = 'game_over'
    game_won = 'game_won'
    game_waiting = 'game_waiting'


class Difficulty(Enum):
    EASY = 1, "easy"
    NORMAL = 2, "normal"
    HARD = 3, "hard"
    HELL = 4, "hell"


class Game:

    def __init__(self, grid):
        self.__grid = grid
        self.__score = 0
        self.__chart = Chart()
        self.__history = []
        self.__state = State.game_waiting
        self.__undo_counter = 0
        self.__difficulty = Difficulty.NORMAL
        self.__slider = {
            'left': self.__grid.slide_left,
            'right': self.__grid.slide_right,
            'up': self.__grid.slide_up,
            'down': self.__grid.slide_down
        }

    def slide_to(self, direction):
        if self.__slider.get(direction) == None:
            return
        try:
            grid_before_slide = self.__grid.copy()
            points_gained, must_generate = self.__slider.get(direction)()
        except GridWinScoreReachedException as e:
            self.__state = State.game_won
            points_gained, must_generate = e.value
        if must_generate:
            self.__history.append((grid_before_slide, points_gained))
            if len(self.__history) > constants.DEFAULT_HISTORY_LENGTH:
                self.__history.pop(0)
            self.__grid.generate_number(self.__difficulty.value[0])
            self.__score += points_gained
        else:
            if not self.__grid.can_slide():
                if self.__state != State.game_won:
                    self.__state = State.game_over

    def undo(self):
        if self.__undo_counter == constants.DEFAULT_HISTORY_LENGTH:
            return
        if len(self.__history) > 0:
            grid, score = self.__history.pop()
            self.__grid = grid
            self.__score -= score
            self.__undo_counter += 1

    def start(self):
        if(self.__state == State.game_waiting):
            self.__grid.generate_number(int(self.__difficulty.value[0]))
            self.__grid.generate_number(int(self.__difficulty.value[0]))
            self.__state = State.running

    def set_difficulty(self, selected):
        self.__difficulty = selected

    def get_value_at(self, position):
        return self.__grid[position]

    def score(self):
        return self.__score

    def reset(self):
        self.__grid.reset()
        self.__history = []
        self.__state = State.running
        self.__score = 0
        self.__undo_counter = 0
        self.start()

    def grid_dimensions(self):
        return self.__grid.dimensions()

    def get_state(self):
        return self.__state

    def change_state(self, state):
        if state in [State.running, State.game_over, State.game_won]:
            self.__state = state

    def undos_left(self):
        return constants.DEFAULT_HISTORY_LENGTH - self.__undo_counter

    def check_score(self):
        return self.__chart.is_top_score(self.__score)

    def add_player_to_chart(self, name, score):
        self.__chart.add(name, score)

    def save_top_scores(self, filename):
        self.__chart.save(filename)

    def load_top_scores(self, filename):
        self.__chart.load(filename)

    def get_top_players(self):
        return self.__chart

    def reset_high_scores(self):
        self.__chart.reset()
