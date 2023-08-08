import os.path
import time

from PyQt5 import QtMultimedia
from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import *
from music import Ui_SimpleMusiPlayer


class SimpleMusicPlayer(QMainWindow, Ui_SimpleMusiPlayer):
    def __init__(self):
        super().__init__()
        self.window = QMainWindow()
        self.setupUi(self)
        self.show()

        # Inits
        self.current_songs = []
        self.current_volume = 50

        global stopped
        stopped = False

        self.player = QtMultimedia.QMediaPlayer()
        self.player.setVolume(self.current_volume)

        # Slider Timer
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.move_slider)

        # Connections
        self.musicSlider.sliderMoved[int].connect(lambda: self.player.setPosition(self.musicSlider.value()))
        self.volumeSlider.sliderMoved[int].connect(lambda: self.volume_changed())
        self.actionAdd_Songs.triggered.connect(self.add_songs)
        self.actionRemove_Selected.triggered.connect(self.remove_one_song)
        self.actionRemove_All.triggered.connect(self.remove_all_songs)
        self.playpushButton.clicked.connect(self.play_song)
        self.pausepushButton.clicked.connect(self.pause_and_unpause)
        self.nextpushButton.clicked.connect(self.next_song)
        self.previouspushButton.clicked.connect(self.previous_song)
        self.stoppushButton.clicked.connect(self.stop_song)

    def move_slider(self):
        if stopped:
            return
        else:
            # Update the slider
            if self.player.state() == QMediaPlayer.PlayingState:
                self.musicSlider.setMinimum(0)
                self.musicSlider.setMaximum(self.player.duration())
                slider_position = self.player.position()
                self.musicSlider.setValue(slider_position)

                current_time = time.strftime('%H:%M:%S', time.localtime(self.player.position() / 1000))
                song_duration = time.strftime('%H:%M:%S', time.localtime(self.player.duration() / 1000))
                self.start_time_label.setText(f"{current_time}")
                self.end_time_label.setText(f"{song_duration}")

    def add_songs(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, caption='Add Songs',
            directory=':\\', filter="Supported Files (*.mp3;*.mpeg;*.ogg;*.m4a;*.MP3;*.wma;*.acc;*.amr)"
        )
        if files:
            for file in files:
                self.current_songs.append(file)
                self.listWidget.addItem(os.path.basename(file))

    def play_song(self):
        try:
            global stopped
            stopped = False

            current_selection = self.listWidget.currentRow()
            current_song = self.current_songs[current_selection]

            song_url = QMediaContent(QUrl.fromLocalFile(current_song))
            self.player.setMedia(song_url)
            self.player.play()
            self.move_slider()
        except Exception as e:
            print(f"Play song error: {e}")

    def pause_and_unpause(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def next_song(self):
        try:
            current_selection = self.listWidget.currentRow()

            if current_selection + 1 == len(self.current_songs):
                next_index = 0
            else:
                next_index = current_selection + 1
            current_song = self.current_songs[next_index]
            self.listWidget.setCurrentRow(next_index)
            song_url = QMediaContent(QUrl.fromLocalFile(current_song))
            self.player.setMedia(song_url)
            self.player.play()
            self.move_slider()
        except Exception as e:
            print(f"Next song error: {e}")

    def previous_song(self):
        try:
            current_selection = self.listWidget.currentRow()

            if current_selection == 0:
                previous_index = len(self.current_songs) - 1
            else:
                previous_index = current_selection - 1

            current_song = self.current_songs[previous_index]
            self.listWidget.setCurrentRow(previous_index)
            song_url = QMediaContent(QUrl.fromLocalFile(current_song))
            self.player.setMedia(song_url)
            self.player.play()
            self.move_slider()
        except Exception as e:
            print(f"Previous song error: {e}")

    def stop_song(self):
        self.player.stop()
        self.musicSlider.setValue(0)
        self.start_time_label.setText(f"00:00:00")
        self.end_time_label.setText(f"00:00:00")

    def volume_changed(self):
        try:
            self.current_volume = self.volumeSlider.value()
            self.player.setVolume(self.current_volume)
            self.volume_label.setText(f"{self.current_volume}")
        except Exception as e:
            print(f"Changing volume error: {e}")

    def remove_one_song(self):
        current_selection = self.listWidget.currentRow()
        self.current_songs.pop(current_selection)
        self.listWidget.takeItem(current_selection)

    def remove_all_songs(self):
        self.stop_song()
        self.listWidget.clear()
        self.current_songs.clear()
