from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import sys
from game import *
from input_dialog import InputDialog

class Tile(QLabel):

    tile_size = 70

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(self.tile_size, self.tile_size)
        self.setAlignment(Qt.AlignCenter)


class Window(QWidget):

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
                tile.setLineWidth(2)
                qGrid.addWidget(tile, x, y)

        score_label = QLabel('Score: {}'.format(self.game.score()))
        score_label.setStyleSheet("""QLabel { font : 14pt;}""")
        undo_label = QLabel('Undo: {}'.format(self.game.undos_left()))
        undo_label.setStyleSheet("""QLabel { font : 14pt;}""")
        qGrid.addWidget(score_label, height, 0, 1, width)
        qGrid.addWidget(undo_label, height + 1, 0, 1, width)

    def keyPressEvent(self, event):
        state = self.game.get_state()
        if state == State.game_waiting:
            return
        key = event.key()
        if state != State.running:
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

        if key == Qt.Key_U:
            self.game.undo()

        self.clear_layout(self.layout())
        self.draw()

    def show_game_over(self):
        self.show_end('Game Over!')

    def show_game_won(self):
        self.show_end('Game Won!')

    def show_end(self, message):
        self.clear_layout(self.layout())
        game_over_label = QLabel(message)
        game_over_label.setStyleSheet(
            """QLabel { font : 25pt; color : red;}""")
        top_score_label = QLabel('Your score is within the top 10!')
        top_score_label.setStyleSheet(
            """QLabel { font : 25pt;}""")
        self.layout().addWidget(game_over_label)
        if self.game.check_score():
            self.layout().addWidget(game_over_label)

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
        self.app = QApplication(sys.argv)
        self.w = Window(self.__game)
        self.w.setWindowTitle('2048')
        self.setup()

    def main_loop(self):

        self.w.draw()
        self.w.show()
        self.app.exec_()

    def setup(self):
        self.w.draw()
        layout = self.w.layout()
        self.cb = QComboBox()
        self.cb.addItems([x.value[1] for x in list(Difficulty)])

        self.btnStart = QPushButton("Start game!")
        self.btnStart.clicked.connect(self.startGame)

        layout.addWidget(self.cb)
        layout.addWidget(self.btnStart)

    def startGame(self):
        self.__game.set_difficulty(self.getSelected())
        self.__game.load_top_scores('data.bin')
        self.__game.start()
        self.cb.setParent(None)
        self.btnStart.setParent(None)
        self.w.draw()

    def getSelected(self):
        for d in list(Difficulty):
            if d.value[1] == self.cb.currentText():
                return d
