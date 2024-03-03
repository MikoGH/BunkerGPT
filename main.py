from design.window_main import *
from modules import *
from player import Player, get_traits_text, get_traits_keys
from story import Story
from texts import Text

story = Story(n_players=6)

app = QApplication(sys.argv)
window = MainWindow(story)
# window.showFullScreen()
window.show()
app.exec()
