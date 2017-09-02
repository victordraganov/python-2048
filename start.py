from grid import Grid
from game import Game
from tui import TextUserInterface
from gui import GraphicUserInterface
import argparse


def main():

    parser = argparse.ArgumentParser(description='The 2048 game.')
    # parser.add_argument(
    #     '--tui', action='store_true', help='starts the game in text mode')

    parser.add_argument('width', type=int,
                        help='Choose grid width')

    parser.add_argument('height', type=int,
                        help='Choose grid height')
    args = parser.parse_args()

    grid = Grid(int(args.width), int(args.height))

    game = Game(grid)

    # if args.tui:
    #     ui = TextUserInterface(game)
    # else:
    ui = GraphicUserInterface(game)

    ui.main_loop()

if __name__ == '__main__':
    main()