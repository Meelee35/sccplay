from PySide6.QtWidgets import QApplication, QMainWindow
from threading import Thread
import subprocess
from main_ui import Ui_MainWindow  # your generated file
from core import play_midi_playlist, init  # your Linux SCCPlay logic

class SCCPlayGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.directory = ""
        self.should_stop = False
        self.playing_thread = None

        self.ui.browseBtn.clicked.connect(self.select_directory)
        self.ui.play.clicked.connect(self.start_playback)
        self.ui.pause.clicked.connect(self.stop_playback)

    def select_directory(self):
        from PySide6.QtWidgets import QFileDialog
        folder = QFileDialog.getExistingDirectory(self, "Select MIDI Folder")
        if folder:
            self.directory = folder
            self.ui.pathEdit.setText(folder)
            self.ui.output.setText(f"Selected folder: {folder}")

    def start_playback(self):
        if not self.directory:
            self.ui.output.setText("Please select a folder first!")
            return
        shuffle = self.ui.shuffle.isChecked()
        loop = self.ui.loop.isChecked()
        self.should_stop = False

        def playback_wrapper():
            # Call your existing core function
            play_midi_playlist(self.directory, shuffle, loop)
            if not self.should_stop:
                self.ui.output.setText("Playback finished.")

        self.playing_thread = Thread(target=playback_wrapper, daemon=True)
        self.playing_thread.start()
        self.ui.output.setText("Playback started...")

    def stop_playback(self):
        self.should_stop = True
        subprocess.call(['pkill', '-f', 'gxscc.exe'])
        self.ui.output.setText("Playback stopped.")


if __name__ == "__main__":
    app = QApplication([])
    window = SCCPlayGUI()
    window.show()
    app.exec()
