import os
import subprocess
import sys
import time

import cv2
import pygame

MAP = os.path.dirname(os.path.abspath(__file__))
MEDIA = os.path.join(MAP, "media")

SCRIPT_TIMEOUT = 30   # script wordt afgebroken na zoveel seconden
MAX_SECONDEN = 10     # maximale duur van de video
MUZIEK_EXTENSIES = (".mp3", ".wav", ".ogg")


def media(naam):
    return os.path.join(MEDIA, naam)


def zoek_muziek(basisnaam):
    """Zoekt succes.mp3 / succes.wav / succes.ogg enz. Geeft None als er niets is."""
    for ext in MUZIEK_EXTENSIES:
        pad = media(basisnaam + ext)
        if os.path.exists(pad):
            return pad
    return None


def laad_geluid(basisnaam):
    pad = zoek_muziek(basisnaam)
    if pad is None:
        print(f"Let op: geen muziek gevonden voor '{basisnaam}', alleen video.")
        return None
    try:
        return pygame.mixer.Sound(pad)
    except pygame.error as e:
        print(f"Let op: kon {os.path.basename(pad)} niet laden ({e}).")
        return None


# Eenmalig klaarzetten bij het opstarten: dit scheelt wachttijd later
try:
    pygame.mixer.init()
    GELUID = {
        True: laad_geluid("succes"),
        False: laad_geluid("fout"),
    }
except pygame.error as e:
    print(f"Let op: geluid niet beschikbaar ({e}).")
    GELUID = {True: None, False: None}


def speel_video(pad):
    if not os.path.exists(pad):
        print(f"Let op: video {os.path.basename(pad)} niet gevonden.")
        return

    cap = cv2.VideoCapture(pad)
    if not cap.isOpened():
        print(f"Let op: kon {os.path.basename(pad)} niet openen.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    venster = "Resultaat"
    cv2.namedWindow(venster, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(venster, cv2.WND_PROP_TOPMOST, 1)

    start = time.time()
    n = 0
    while time.time() - start < MAX_SECONDEN:
        ok, frame = cap.read()
        if not ok:
            break
        cv2.imshow(venster, frame)
        n += 1
        wacht = max(1, int((start + n / fps - time.time()) * 1000))
        toets = cv2.waitKey(wacht) & 0xFF
        if toets in (27, ord("q")):  # Esc of q sluit het venster
            break
        if cv2.getWindowProperty(venster, cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    cv2.destroyAllWindows()


def voer_uit(script):
    try:
        resultaat = subprocess.run(
            [sys.executable, script],
            capture_output=True,
            text=True,
            timeout=SCRIPT_TIMEOUT,
        )
        gelukt = resultaat.returncode == 0
        uitvoer, fouten = resultaat.stdout, resultaat.stderr
    except subprocess.TimeoutExpired:
        gelukt = False
        uitvoer = ""
        fouten = f"Script duurde langer dan {SCRIPT_TIMEOUT} seconden."

    print("--- Uitvoer ---")
    print(uitvoer)
    if gelukt:
        print("Gelukt!")
    else:
        print("Fout!")
        print(fouten)

    geluid = GELUID[gelukt]
    if geluid:
        geluid.play()
    speel_video(media("succes.mp4" if gelukt else "fout.mp4"))
    if geluid:
        geluid.stop()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Gebruik: py runner.py naam_van_script.py")
    else:
        voer_uit(sys.argv[1])