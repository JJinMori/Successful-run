import os
import subprocess

import imageio_ffmpeg

MAP = os.path.dirname(os.path.abspath(__file__))
MEDIA = os.path.join(MAP, "media")
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

for naam in ("succes", "fout"):
    video = os.path.join(MEDIA, naam + ".mp4")
    audio = os.path.join(MEDIA, naam + ".mp3")

    if not os.path.exists(video):
        print(f"{naam}.mp4 niet gevonden, overgeslagen.")
        continue

    print(f"Bezig met {naam}.mp4 ...")
    resultaat = subprocess.run(
        [FFMPEG, "-y", "-i", video, "-vn", "-acodec", "libmp3lame", "-q:a", "2", audio],
        capture_output=True,
        text=True,
    )
    if resultaat.returncode == 0:
        print(f"Klaar: {naam}.mp3")
    else:
        print(f"Mislukt voor {naam}.mp4:")
        print(resultaat.stderr[-500:])