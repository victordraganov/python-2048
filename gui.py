from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, \
    QFrame, QWidgetItem
import sys
from game import State


class Tile(QLabel):

    tile_size = 70

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(self.tile_size, self.tile_size)
        self.setAlignment(Qt.AlignCenter)


class Grid(QWidget):

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.width, self.height = game.grid_dimensions()
        qGrid = QGridLayout()
        self.setLayout(qGrid)
        qGrid.setSpacing(5)

    def draw(self):
        qGrid = self.layout()
        width, height = self.width, self.height

        for x in range(height):
            for y in range(width):
                value = self.game.get_value_at((x, y))
                if value:
                    tile = Tile(str(value))
                else:
                    tile = Tile(str(''))
                tile.value = value
                tile.position = (x, y)
                tile.setFrameShape(QFrame.Box)
                tile.setStyleSheet("""QLabel { font : 20pt;}""")
                tile.setLineWidth(3)
                qGrid.addWidget(tile, x, y)

        score_label = QLabel('Score: {}'.format(self.game.score()))
        score_label.setStyleSheet("""QLabel { font : 14pt;}""")
        undo_label = QLabel('Undo: {}'.format(self.game.undos_left()))
        undo_label.setStyleSheet("""QLabel { font : 14pt;}""")
        qGrid.addWidget(score_label, height, 0, 1, width)
        qGrid.addWidget(undo_label, height + 1, 0, 1, width)

    def keyPressEvent(self, event):

        key = event.key()
        if self.game.get_state() != State.running:
            if self.game.get_state() == State.game_won:
                self.show_game_won()
            else:
                self.show_game_over()
            return
        if key == Qt.Key_Left:
            self.game.slide_to('left')

        if key == Qt.Key_Down:
            self.game.slide_to('down')

        if key == Qt.Key_Up:
            self.game.slide_to('up')

        if key == Qt.Key_Right:
            self.game.slide_to('right')

        if key == Qt.Key_R:
            self.game.reset()

        if key == Qt.Key_Z:
            self.game.undo()

        self.clear_layout(self.layout())
        self.draw()

    def show_game_over(self):
        self.clear_layout(self.layout())
        game_over_label = QLabel('Game Over!')
        game_over_label.setStyleSheet(
            """QLabel { font : 25pt; color : red;}""")
        top_score_label = QLabel('Your score is within the top 10!')
        top_score_label.setStyleSheet(
            """QLabel { font : 25pt;}""")
        self.layout().addWidget(game_over_label)
        if self.game.check_score():
            self.layout().addWidget(game_over_label)

    def show_game_won(self):
        pass

    def show_high_scores(self):
        self.game.get_top_players()

    def clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)

            if isinstance(item, QWidgetItem):
                item.widget().close()
            else:
                self.clear_layout(item.layout())
            layout.removeItem(item)


class GraphicUserInterface():

    def __init__(self, game):
        self.__game = game

    def main_loop(self):
        app = QApplication(sys.argv)
        w = Grid(self.__game)
        self.__game.load_top_scores('data.bin')
        self.__game.start()
        w.setWindowTitle('Clumsy')
        w.draw()
        w.show()
        app.exec_()