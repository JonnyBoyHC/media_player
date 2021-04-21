from PyQt5.QtWidgets import QApplication, QWidget, QStyle, QSizePolicy, QFileDialog, QPushButton, QHBoxLayout, \
    QVBoxLayout, QLabel, QSlider
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QVideoSurfaceFormat
from PyQt5.QtGui import QIcon, QPalette
import sys
import pafy


# Grab url link content from youtube
url = 'https://www.youtube.com/watch?v=oCKrKtk-rDw'
video = pafy.new(url)
best = video.getbest()
play_url = best.url


class Window(QWidget):
    def __init__(self):
        super().__init__()

        # Set window interface
        self.setWindowTitle("COMP6125 - Group Assignment 1 - Media Player")
        self.setGeometry(400, 150, 800, 550)
        self.setWindowIcon(QIcon('player.png'))
        self.label = QLabel()
        self.play_Btn = QPushButton()
        self.stop_Btn = QPushButton()
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.slider = QSlider(Qt.Horizontal)

        # Set Background to black color
        bg_color = self.palette()
        bg_color.setColor(QPalette.Window, Qt.black)
        self.setPalette(bg_color)

        # Set media player objects
        self.init_ui()
        self.show()

    def init_ui(self):
        # Create media player object

        # Create video widget object
        video_widget = QVideoWidget()

        # Create open button
#         open_btn = QPushButton('Open Link')
#         open_btn.clicked.connect(self.open_file)

        # Create button for stopping
        self.stop_Btn.setEnabled(True)
        self.stop_Btn.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.stop_Btn.clicked.connect(self.stop_video)

        # Create button for playing
        self.play_Btn.setEnabled(True)
        self.play_Btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_Btn.clicked.connect(self.play_video)

        # Create slider
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)

        # Create label
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # Create horizontal box layout
        hbox_Layout = QHBoxLayout()
        hbox_Layout.setContentsMargins(0, 0, 0, 0)

        # Set widgets to the horizontal box layout
#         hbox_Layout.addWidget(open_btn)
        hbox_Layout.addWidget(self.stop_Btn)
        hbox_Layout.addWidget(self.play_Btn)
        hbox_Layout.addWidget(self.slider)

        # Create vertical box layout
        vbox_Layout = QVBoxLayout()
        vbox_Layout.addWidget(video_widget)
        vbox_Layout.addLayout(hbox_Layout)
        vbox_Layout.addWidget(self.label)

        self.setLayout(vbox_Layout)
        self.mediaPlayer.setVideoOutput(video_widget)

        # Media player signals
        self.mediaPlayer.stateChanged.connect(self.video_state_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

        # Get video content from pafy url
        self.mediaPlayer.setMedia(QMediaContent(QUrl(play_url)))

#     def open_file(self):
#         file_name, _ = QFileDialog.getOpenFileName(self, "Open Link")
# 
#         if file_name != '':
#             self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(file_name)))
#             self.play_Btn.setEnabled(True)
#             self.stop_Btn.setEnabled(True)
#             print(f'\nVideo Loaded from: \n{file_name}\n')

    def stop_video(self):
        self.mediaPlayer.stop()
        print(f'Stopped!!!')

    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            print(f'Paused.')
        else:
            self.mediaPlayer.play()
            print(f'Playing...')

    def video_state_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.play_Btn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)
            )
        else:
            self.play_Btn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)
            )

    def position_changed(self, position):
        self.slider.setValue(position)

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def handle_errors(self):
        self.play_Btn.setEnabled(False)
        self.label.setText("Error: " + self.mediaPlayer.errorString())


app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())