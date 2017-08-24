import unittest
from game import Game,State
from grid import Grid
from chart import Chart
from exceptions import *
from copy import deepcopy

class ChartTests(unittest.TestCase):

    def setUp(self):
        self.test_chart = Chart()

    def test_empty_chart(self):
        for top_player in self.test_chart:
            self.assertEqual(top_player[0], '')
            self.assertEqual(top_player[1], 0)

    def test_chart_add(self):
        self.test_chart.add('User1', 100)
        self.test_chart.add('User2', 200)
        self.test_chart.add('User3', 300)
        self.test_chart.add('User4', 400)
        self.test_chart.add('User5', 500)
        self.test_chart.add('User6', 600)
        self.test_chart.add('User7', 700)
        self.test_chart.add('User8', 800)
        self.test_chart.add('User9', 900)
        self.test_chart.add('User10', 1000)
        self.test_chart.add('User11', 50)
        for index in range(10):
            self.assertEqual(
                self.test_chart.top_players[index][0],
                ('User' + str(10 - index)))
            self.assertEqual(
                self.test_chart.top_players[index][1], (1000 - index * 100))
        for top_player in self.test_chart.top_players:
            self.assertNotEqual(top_player[0], 'User11')

    def test_chart_is_top_score(self):
        self.test_chart.add('User1', 100)
        self.test_chart.add('User2', 200)
        self.test_chart.add('User3', 300)
        self.test_chart.add('User4', 400)
        self.test_chart.add('User5', 500)
        self.test_chart.add('User6', 600)
        self.test_chart.add('User7', 700)
        self.test_chart.add('User8', 800)
        self.test_chart.add('User9', 900)
        self.test_chart.add('User10', 1000)
        self.assertTrue(self.test_chart.is_top_score(1500))
        self.assertTrue(self.test_chart.is_top_score(500))
        self.assertTrue(self.test_chart.is_top_score(100))
        self.assertFalse(self.test_chart.is_top_score(50))

    def test_chart_reset(self):
        self.test_chart.add('User1', 100)
        self.test_chart.add('User2', 200)
        self.test_chart.add('User3', 300)
        self.test_chart.add('User4', 400)
        self.test_chart.add('User5', 500)
        self.test_chart.add('User6', 600)
        self.test_chart.add('User7', 700)
        self.test_chart.add('User8', 800)
        self.test_chart.add('User9', 900)
        self.test_chart.add('User10', 1000)
        self.test_chart.reset()
        for top_player in self.test_chart:
            self.assertEqual(top_player[0], '')
            self.assertEqual(top_player[1], 0)

    def test_chart_save(self):
        self.test_chart.add('User10', 100)
        self.test_chart.add('User9', 200)
        self.test_chart.add('User8', 300)
        self.test_chart.add('User7', 400)
        self.test_chart.add('User6', 500)
        self.test_chart.add('User5', 600)
        self.test_chart.add('User4', 700)
        self.test_chart.add('User3', 800)
        self.test_chart.add('User2', 900)
        self.test_chart.add('User1', 1000)
        self.test_chart.save('save_test.dat')
        import os
        self.assertTrue(os.path.isfile('save_test.dat'))

    def test_chart_load(self):
        self.test_chart.load('save_test.dat')
        for index in range(10):
            self.assertEqual(
                self.test_chart.top_players[index][0],
                ('User' + str(index + 1)))
            self.assertEqual(
                self.test_chart.top_players[index][1], (1000 - index * 100))


class GameTests(unittest.TestCase):

    def setUp(self):
        self.height = 4
        self.width = 4
        grid = Grid(self.width, self.height)
        self.test_game = Game(grid)

    def test_start(self):
        self.test_game.start()
        counter = 0
        for x in range(self.height):
            for y in range(self.width):
                if self.test_game.get_value_at((x, y)) != 0:
                    counter += 1
        self.assertEqual(counter, 2)

    def test_grid_dimensions(self):
        self.assertEqual(
            self.test_game.grid_dimensions(), (self.width, self.height))

    def test_reset(self):
        self.test_game.reset()
        self.assertEqual(self.test_game._Game__history, [])
        self.assertEqual(self.test_game._Game__state, State.running)
        self.assertEqual(self.test_game._Game__score, 0)
        self.assertEqual(self.test_game._Game__undo_counter, 0)

    def test_undo(self):
        self.test_game.start()
        self.test_game.slide_to('left')
        saved_state = deepcopy(self.test_game._Game__grid._Grid__cells)
        self.test_game.slide_to('right')
        self.test_game.slide_to('up')
        self.test_game.slide_to('down')
        self.test_game.undo()
        self.test_game.undo()
        self.test_game.undo()
        self.test_game.undo()
        self.assertEqual(saved_state, self.test_game._Game__grid._Grid__cells)
        self.assertEqual(self.test_game.undos_left(), 0)

    def test_game_won(self):
        self.test_game.start()
        self.test_game.slide_to('invalid')
        self.test_game._Game__grid._Grid__cells = [[1024, 1024, 2, 2],
                                                   [1024, 2, 4, 0],
                                                   [4, 0, 2, 2],
                                                   [4, 2, 0, 4]]
        self.test_game.slide_to('left')
        self.assertEqual(self.test_game.get_state(), State.game_won)

    def test_game_over(self):
        self.test_game._Game__grid._Grid__cells = [[2, 4, 8, 2],
                                                   [8, 2, 4, 16],
                                                   [2, 16, 8, 2],
                                                   [4, 8, 2, 4]]
        self.test_game.slide_to('left')
        self.assertEqual(self.test_game.get_state(), State.game_over)

    def test_change_state(self):
        self.test_game.change_state(State.game_won)
        self.assertEqual(self.test_game.get_state(), State.game_won)

    def test_check_score(self):
        self.test_game.load_top_scores('save_test.dat')
        self.test_game._Game__score = 500
        self.assertTrue(self.test_game.check_score())
        self.assertTrue(self.test_game.score() == 500)


if __name__ == '__main__':
    unittest.main()