from game import State
from utils import getch
from re import match


class TextUserInterface:

    def __init__(self, game):
        self.__game = game

    def print_grid(self):
        width, height = self.__game.grid_dimensions()
        for x in range(height):
            for y in range(width):
                value = self.__game.get_value_at((x, y))
                print('[{}{}]'.format(
                    ' ' * (4 - len(str(value))), value if value != 0 else ' '), end=' ')
            print()

    def print_data(self):
        print('Score: {}'.format(self.__game.score()),
              'Undos left: {}'.format(self.__game.undos_left()))

    def clear_screen(self):
        print('\033c')

    def print_high_scores(self):
        for player in enumerate(self.__game.get_top_players()):
            if player[1][0] != '':
                print(
                    '{}. {} {}'.format(
                        player[0] + 1,
                        player[1][0],
                        player[1][1]))
        print()

    def user_input(self, key):
        key = key.lower()
        commands = {'a': (self.__game.slide_to, ['left']),
                    's': (self.__game.slide_to, ['down']),
                    'd': (self.__game.slide_to, ['right']),
                    'w': (self.__game.slide_to, ['up']),
                    'u': (self.__game.undo, []),
                    'r': (self.__game.reset, [])
                    }
        if key in commands:
            commands[key][0](*commands[key][1])

    def refresh(self):
        self.clear_screen()
        self.print_grid()
        self.print_data()

    def main_loop(self):
        self.__game.load_top_scores('data.bin')
        self.__game.start()
        while self.__game.get_state() == State.running:
            self.refresh()
            char = getch()
            self.user_input(char)
            if char == chr(26):
                break

            if self.__game.get_state() == State.game_over:
                print('Game Over!')
                if self.__game.check_score():
                    print('Your score is within the top 10!')
                    print('Enter your name:')
                    name = input()
                    score = self.__game.score()
                    while not match(r'[a-zA-Z0-9]', name):
                        print('\'{}\' is not a valid name.'.format(name))
                        print('Please try again.')
                        print('Enter your name:')
                        name = input()
                    self.__game.add_player_to_chart(name, score)
                    print('\nHigh Scores')
                    self.print_high_scores()
                    self.__game.save_top_scores('data.bin')
                print('Do you want to play again? y/n')
                choice = input()
                if choice == 'y' or choice == 'Y':
                    self.__game.change_state(State.running)
                    self.__game.reset()

            if self.__game.get_state() == State.game_won:
                self.refresh()
                print('Congratulations! You reached 2048!')
                print('Do you want to continue to play? y/n')
                choice = input()
                if choice == 'y' or choice == 'Y':
                    self.__game.change_state(State.running)
                else:
                    if self.__game.check_score():
                        print('Your score is within the top 10!')
                        print('Enter your name:')
                        name = input()
                        score = self.__game.score()
                        while not match(r'[a-zA-Z0-9]', name):
                            print('\'{}\' is not a valid name.'.format(name))
                            print('Please try again.')
                            print('Enter your name:')
                            name = input()
                        self.__game.add_player_to_chart(name, score)
                        print('\nHigh Scores')
                        self.print_high_scores()
                        self.__game.save_top_scores('data.bin')
