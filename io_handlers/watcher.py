import os
from PyQt6.QtCore import QThread, pyqtSignal
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class WatchdogHandler(FileSystemEventHandler):
    def __init__(self, target_path: str, callback):
        self.target_path = os.path.normcase(os.path.abspath(target_path))
        self.callback = callback

    def check_and_emit(self, path):
        if os.path.normcase(os.path.abspath(path)) == self.target_path:
            self.callback()

    def on_modified(self, event):
        if not event.is_directory:
            self.check_and_emit(event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            self.check_and_emit(event.dest_path)

class FileWatcher(QThread):
    file_changed = pyqtSignal(str)

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = os.path.normcase(os.path.abspath(file_path))
        self.directory = os.path.dirname(self.file_path)
        self.observer = None

    def run(self):
        handler = WatchdogHandler(self.file_path, lambda: self.file_changed.emit(self.file_path))
        self.observer = Observer()
        self.observer.schedule(handler, self.directory, recursive=False)
        self.observer.start()
        self.exec()

    def stop(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()
        self.quit()
        self.wait()
