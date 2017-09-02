import unittest
from grid import *


class GridSlideTest(unittest.TestCase):

    def setUp(self):
        self.test_grid = Grid(4, 4)
        self.sample_grids_before_slide = [[[2, 2, 2, 2],
                                           [0, 2, 4, 0],
                                           [4, 0, 2, 2],
                                           [4, 2, 0, 4]],

                                          [[4, 0, 2, 4],
                                           [0, 0, 0, 0],
                                           [4, 2, 2, 2],
                                           [4, 0, 0, 2]],

                                          [[2, 0, 0, 2],
                                           [0, 2, 4, 4],
                                           [4, 2, 0, 2],
                                           [4, 8, 2, 4]]]

    def test_slide_left(self):
        sample_grids_after_slide = [[[4, 4, 0, 0],
                                     [2, 4, 0, 0],
                                     [4, 4, 0, 0],
                                     [4, 2, 4, 0]],

                                    [[4, 2, 4, 0],
                                     [0, 0, 0, 0],
                                     [4, 4, 2, 0],
                                     [4, 2, 0, 0]],

                                    [[4, 0, 0, 0],
                                     [2, 8, 0, 0],
                                     [4, 4, 0, 0],
                                     [4, 8, 2, 4]]]
        for x in range(len(self.sample_grids_before_slide)):
            self.test_grid._Grid__cells = self.sample_grids_before_slide[x]
            self.test_grid.slide_left()
            self.assertEqual(
                self.test_grid._Grid__cells, sample_grids_after_slide[x])

    def test_slide_right(self):
        sample_grids_after_slide = [[[0, 0, 4, 4],
                                     [0, 0, 2, 4],
                                     [0, 0, 4, 4],
                                     [0, 4, 2, 4]],

                                    [[0, 4, 2, 4],
                                     [0, 0, 0, 0],
                                     [0, 4, 2, 4],
                                     [0, 0, 4, 2]],

                                    [[0, 0, 0, 4],
                                     [0, 0, 2, 8],
                                     [0, 0, 4, 4],
                                     [4, 8, 2, 4]]]

        for x in range(len(self.sample_grids_before_slide)):
            self.test_grid._Grid__cells = self.sample_grids_before_slide[x]
            self.test_grid.slide_right()
            self.assertEqual(
                self.test_grid._Grid__cells, sample_grids_after_slide[x])

    def test_slide_up(self):
        sample_grids_after_slide = [[[2, 4, 2, 4],
                                     [8, 2, 4, 4],
                                     [0, 0, 2, 0],
                                     [0, 0, 0, 0]],

                                    [[8, 2, 4, 4],
                                     [4, 0, 0, 4],
                                     [0, 0, 0, 0],
                                     [0, 0, 0, 0]],

                                    [[2, 4, 4, 2],
                                     [8, 8, 2, 4],
                                     [0, 0, 0, 2],
                                     [0, 0, 0, 4]]]

        for x in range(len(self.sample_grids_before_slide)):
            self.test_grid._Grid__cells = self.sample_grids_before_slide[x]
            self.test_grid.slide_up()
            self.assertEqual(
                self.test_grid._Grid__cells, sample_grids_after_slide[x])

    def test_slide_down(self):
        sample_grids_after_slide = [[[0, 0, 0, 0],
                                     [0, 0, 2, 0],
                                     [2, 2, 4, 4],
                                     [8, 4, 2, 4]],

                                    [[0, 0, 0, 0],
                                     [0, 0, 0, 0],
                                     [4, 0, 0, 4],
                                     [8, 2, 4, 4]],

                                    [[0, 0, 0, 2],
                                     [0, 0, 0, 4],
                                     [2, 4, 4, 2],
                                     [8, 8, 2, 4]]]
        for x in range(len(self.sample_grids_before_slide)):
            self.test_grid._Grid__cells = self.sample_grids_before_slide[x]
            self.test_grid.slide_down()
            self.assertEqual(
                self.test_grid._Grid__cells, sample_grids_after_slide[x])


class GridGenerateNumberTest(unittest.TestCase):

    def setUp(self):
        height = 4
        width = 4
        self.test_grid = Grid(width, height)
        self.total_cells = width * height

    def test_free_cells_decrease(self):
        for count in range(self.total_cells):
            self.assertEqual(
                len(self.test_grid._Grid__free_cells),
                self.total_cells - count)
            self.test_grid.generate_number(1)

    def test_generate_number_on_full_grid(self):
        for count in range(self.total_cells - 1):
            self.test_grid.generate_number(1)
        self.assertRaises(Exception, self.test_grid.generate_number(1))


class GridSlidePointsTest(unittest.TestCase):

    def setUp(self):
        height = 4
        width = 4
        self.test_grid = Grid(width, height)
        self.sample_grids = [[[2, 2, 2, 2],
                              [0, 2, 4, 0],
                              [4, 0, 2, 2],
                              [4, 2, 0, 4]],

                             [[4, 0, 2, 4],
                              [0, 0, 0, 0],
                              [4, 2, 2, 2],
                              [4, 0, 0, 2]],

                             [[2, 0, 0, 2],
                              [0, 2, 4, 4],
                              [4, 2, 0, 2],
                              [4, 8, 2, 4]]]

    def test_slide_left_points_recieved(self):
        sample_grids_scores = [12, 4, 16]
        for x in range(len(self.sample_grids)):
            self.test_grid._Grid__cells = self.sample_grids[x]
            self.assertEqual(
                self.test_grid.slide_left()[0], sample_grids_scores[x])

    def test_slide_right_points_recieved(self):
        sample_grids_scores = [12, 4, 16]
        for x in range(len(self.sample_grids)):
            self.test_grid._Grid__cells = self.sample_grids[x]
            self.assertEqual(
                self.test_grid.slide_right()[0], sample_grids_scores[x])

    def test_slide_up_points_recieved(self):
        sample_grids_scores = [16, 16, 12]
        for x in range(len(self.sample_grids)):
            self.test_grid._Grid__cells = self.sample_grids[x]
            self.assertEqual(
                self.test_grid.slide_up()[0], sample_grids_scores[x])

    def test_slide_down_points_recieved(self):
        sample_grids_scores = [16, 16, 12]
        for x in range(len(self.sample_grids)):
            self.test_grid._Grid__cells = self.sample_grids[x]
            self.assertEqual(
                self.test_grid.slide_down()[0], sample_grids_scores[x])


class GridCanSlideTest(unittest.TestCase):

    def test_can_slide_grid(self):
        self.test_grid = Grid(4, 4)
        cant_slide_grid = [[2, 4, 8, 2],
                           [8, 2, 4, 16],
                           [2, 16, 8, 2],
                           [4, 8, 2, 4]]
        can_slide_grid = [[2, 0, 0, 2],
                          [0, 2, 4, 4],
                          [4, 2, 0, 2],
                          [4, 8, 2, 4]]
        self.test_grid._Grid__cells = cant_slide_grid
        self.assertFalse(self.test_grid.can_slide())
        self.test_grid._Grid__cells = can_slide_grid
        self.assertTrue(self.test_grid.can_slide())


if __name__ == '__main__':
    unittest.main()