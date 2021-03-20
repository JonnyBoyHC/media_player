from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, \
    QLabel, QSlider, QStyle, QSizePolicy, QFileDialog
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()

        # Set window interface
        self.label = QLabel()
        self.playBtn = QPushButton()
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.slider = QSlider(Qt.Horizontal)
        self.setWindowTitle("COMP6125 - Group Assignment 1 - Media Player")
        self.setGeometry(350, 100, 700, 500)
        self.setWindowIcon(QIcon('player.png'))

        # Set Background to black color
        bg_color = self.palette()
        bg_color.setColor(QPalette.Window, Qt.black)
        self.setPalette(bg_color)

        self.init_ui()
        self.show()

    def init_ui(self):
        # Create media player object

        # Create videowidget object
        videowidget = QVideoWidget()

        # Create open button
        open_btn = QPushButton('Open Video')
        open_btn.clicked.connect(self.open_file)

        # Create button for playing
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)

        # Create slider
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)

        # Create label
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # Create hbox layout
        hbox_Layout = QHBoxLayout()
        hbox_Layout.setContentsMargins(0, 0, 0, 0)

        # Set widgets to the hbox layout
        hbox_Layout.addWidget(open_btn)
        hbox_Layout.addWidget(self.playBtn)
        hbox_Layout.addWidget(self.slider)

        # Create vbox layout
        vbox_Layout = QVBoxLayout()
        vbox_Layout.addWidget(videowidget)
        vbox_Layout.addLayout(hbox_Layout)
        vbox_Layout.addWidget(self.label)

        self.setLayout(vbox_Layout)
        self.mediaPlayer.setVideoOutput(videowidget)

        # Media player signals
        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")

        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)

    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(
                self.style().standardIcon((QStyle.SP_MediaPause))
            )
        else:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)
            )

    def position_changed(self, position):
        self.slider.setValue(position)

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Error: " + self.mediaPlayer.errorString())


app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())
