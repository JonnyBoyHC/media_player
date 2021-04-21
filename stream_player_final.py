from PyQt5.QtWidgets import QApplication, QWidget, QStyle, QSizePolicy, QFileDialog, QPushButton, QHBoxLayout, \
    QVBoxLayout, QLabel, QSlider, QLineEdit, QStatusBar
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import QIcon, QPalette
import sys
import pafy
import validators


class Window(QWidget):
    def __init__(self):
        super().__init__()

        # Set window interface
        self.setWindowTitle("COMP6125 - Group Assignment 1 - Media Player")
        self.setGeometry(400, 150, 800, 550)
        self.setWindowIcon(QIcon('player.png'))
        self.label = QLabel()
        self.textbox = QLineEdit('Please paste new youtube link here...')
        self.open_Btn = QPushButton()
        self.play_Btn = QPushButton()
        self.stop_Btn = QPushButton()
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.slider = QSlider(Qt.Horizontal)
        
        # Grab url link content from youtube
        self.url = 'https://www.youtube.com/watch?v=oCKrKtk-rDw'
        self.video = pafy.new(self.url)
        self.best = self.video.getbest()
        self.play_url = self.best.url
        print(f'\nLoaded Url Link: \n{self.play_url}\n')

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
        
        # Create text box
        self.textbox.setReadOnly(False)
        
        # Create button to open link
        self.open_Btn.setEnabled(True)
        self.open_Btn.setText("Open Link")
        self.open_Btn.clicked.connect(self.get_link)

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
        hbox_Layout.addWidget(self.open_Btn)
        hbox_Layout.addWidget(self.stop_Btn)
        hbox_Layout.addWidget(self.play_Btn)
        hbox_Layout.addWidget(self.slider)

        # Create vertical box layout
        vbox_Layout = QVBoxLayout()
        vbox_Layout.addWidget(video_widget)
        vbox_Layout.addWidget(self.textbox)
        vbox_Layout.addLayout(hbox_Layout)
        vbox_Layout.addWidget(self.label)

        # Setup layout
        self.setLayout(vbox_Layout)
        self.mediaPlayer.setVideoOutput(video_widget)

        # Media player signals
        self.mediaPlayer.stateChanged.connect(self.video_state_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)
        
        # Set URL link to playing content
        self.mediaPlayer.setMedia(QMediaContent(QUrl(self.play_url)))

    def stop_video(self):
        self.mediaPlayer.stop()
        print(f'Stopped!!!\n')
        
    def get_link(self):
        # Grab new url link content from the text box
        self.url = self.textbox.text()
        
        # Validate if the new url link is true, then update new link
        try:
            if validators.url(self.url) == True and self.url[:32] == 'https://www.youtube.com/watch?v=':
                self.video = pafy.new(self.url)
                self.best = self.video.getbest()
                self.play_url = self.best.url
                self.mediaPlayer.setMedia(QMediaContent(QUrl(self.play_url)))
                print(f'\nLoaded Url Link: \n{self.play_url}\n')
            else:
                print(f'\nInvalid Url Link, please try again!!!\n')
        except:
            print(f'\nInvalid Url Link, please try again!!!\n')

    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            print(f'Paused.\n')
        else:
            self.mediaPlayer.play()
            print(f'Playing...')
            print(f'Title: {self.video.title}')
            print(f'Rating: {self.video.rating}; Viewcount: {self.video.viewcount}; Author: {self.video.author}'
                  f'\nLength: {self.video.duration}; Likes: {self.video.likes}; Dislikes: {self.video.dislikes}')
            print(f'Resolution: {self.best.resolution}')
            print(f'Video Format: {self.best.extension}')
            print(f'File Size: {round(self.best.get_filesize()/1024**2,2)}MB')
            print("\n")
            
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