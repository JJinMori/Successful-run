import os
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

import runner  # laadt cv2 en pygame al bij het opstarten

MAP = os.path.dirname(os.path.abspath(__file__))
NEGEER = {"runner.py", "watcher.py"}
WACHT_TUSSEN_RUNS = 3  # seconden, om dubbele triggers te vermijden


class ScriptHandler(FileSystemEventHandler):
    def __init__(self):
        self.laatste_run = 0

    def on_modified(self, event):
        if event.is_directory or not event.src_path.endswith(".py"):
            return
        naam = os.path.basename(event.src_path)
        if naam in NEGEER:
            return
        if time.time() - self.laatste_run < WACHT_TUSSEN_RUNS:
            return

        self.laatste_run = time.time()
        print(f"\n>>> {naam} opgeslagen, uitvoeren...")
        try:
            runner.voer_uit(event.src_path)
        except Exception as e:
            print(f"Onverwachte fout in de watcher: {e}")
        self.laatste_run = time.time()


if __name__ == "__main__":
    observer = Observer()
    observer.schedule(ScriptHandler(), MAP, recursive=False)
    observer.start()
    print(f"Bezig met kijken naar {MAP} ... (Ctrl+C om te stoppen)")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()