# core.py
import shutil
import os, time, subprocess, random
from pathlib import Path
import mido
import sys

def play_midi_playlist(directory, shuffle=False, loop=False, log_callback=print):
    """Play MIDI files in a directory with optional logging callback."""

    def get_midi_files():
        return [str(f) for f in Path(directory).iterdir() if f.is_file() and f.suffix.lower() in ['.mid', '.midi']]

    def get_midi_length(midi_file):
        try:
            return mido.MidiFile(midi_file).length
        except Exception:
            return None

    midi_files = get_midi_files()
    if not midi_files:
        log_callback("No MIDI files found.")
        return

    if shuffle:
        random.shuffle(midi_files)

    midi_lengths = [(f, get_midi_length(f)) for f in midi_files]

    while True:
        for midi_file, length in midi_lengths:
            if length is None:
                log_callback(f"Skipping {midi_file}")
                continue

            wine_path = "Z:" + midi_file.replace("/", "\\")
            subprocess.Popen(
                ['gxscc', wine_path],
                env={**os.environ, 'WINEDEBUG': '-all'},
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            log_callback(f"Playing {os.path.basename(midi_file)} for {round(length)} seconds")
            time.sleep(length)

        if not loop:
            break

def init():
	if shutil.which('gxscc') is None:
		print("GXSCC was not found in \"~/.local/bin\" or \"/usr/local/bin\".", flush=True)
		sys.exit(1)
  try:
    subprocess.Popen(['gxscc'], shell=True)
  except Exception as e:
    print(f"Failed to launch GXSCC.", flush=True)
    sys.exit(e)
  print("Waiting for GXSCC to launch...", flush=True)
  secs = 0
  while True:
      try:
          uuid = subprocess.check_output(['kdotool', 'search', '--name', 'GXSCC']).decode().strip()
          if uuid != '':
            print("GXSCC launched successfully.", flush=True)
            break
          else:
            if secs.is_integer():
              print(f"Waiting {int(secs)} seconds...", flush=True)
      except subprocess.CalledProcessError:
          print("GXSCC window not found.")
      time.sleep(0.5)
      secs += 0.5
      if secs > 20:
        print("GXSCC took too long. Exiting.", flush=True)
        subprocess.call(['pkill', '-f', 'gxscc.exe'])
        sys.exit(1)
  subprocess.call(['kdotool', 'windowminimize', f'{uuid}'])