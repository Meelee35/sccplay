# LINUX BUILD. This is the LINUX version of SCCPlay. It is currently under construction.

# There's probably a better way to write this without so many imports
import argparse
import mido
import os
from pathlib import Path
import random
import subprocess
import time
import sys
import signal
import shutil

def vprint(*args, **kwargs):
   if VERBOSE:
      print("[VERBOSE]", *args, **kwargs)

# I am going to admit this is the first and only time chatgpt was used here. This code just iterates through all files in adirectory and adds midi files to an array.
def get_midi_files(directory):
    p = Path(directory)
    return [str(f) for f in p.iterdir() if f.is_file() and f.suffix.lower() in ['.mid', '.midi']]

# Get the length of midi files, Type 2 midi files are weird so they are ignored
def get_midi_length_seconds(midi_file):
    mid = mido.MidiFile(midi_file)
    try:
        return mid.length
    except ValueError:
        print(f"Cannot get length for asynchronous (type 2) MIDI: {midi_file}", flush=True)
        return None

# Get the lengths of all the midi files so we can know when they end
def generate_lengths(midi_files):
    lengths = []
    for midi_file in midi_files:
        try:
            length = get_midi_length_seconds(midi_file)
            lengths.append((midi_file, length))
            vprint(f"{os.path.basename(midi_file)}: {length} seconds", flush=True)
        except Exception as e:
            print(f"Error processing {midi_file}: {e}", flush=True)
    return lengths


def main():
  # Command line arguments
  parser = argparse.ArgumentParser(description="Play a playlist of midi files in GXSCC.")
  parser.add_argument("-d", "--dir", help="Optional: Midi Directory", default="")
  parser.add_argument("-s", "--shuffle", help="Optional: Shuffle Midi files", action="store_true")
  parser.add_argument("-l", "--loop", help="Optional: Loop Midi files", action="store_true")
  parser.add_argument("-v", "--verbose", help="Optional: Verbose Output", action="store_true")
  args = parser.parse_args()
  
  # Edge case: gxscc not in path.
  if shutil.which('gxscc') is None:
    print("GXSCC was not found in \"~/.local/bin\" or \"/usr/local/bin\".", flush=True)
    sys.exit(1)
    
  # Did the user specify a directory
  if args.dir == '':
    directory = os.getcwd()
  else:
    directory = args.dir
  loop = args.loop

  global VERBOSE
  if args.verbose:
    VERBOSE = True
  else:
    VERBOSE = False

  # Check if the directory has any midi files at all
  midi_files = get_midi_files(directory)
  if not midi_files:
    print("No MIDI files found in the specified directory.", flush=True)
    return
  
    # Launch gxscc beforehand to avoid delay
  print("Launching GXSCC...", flush=True)
  try:
    subprocess.Popen(
        ['nohup', 'gxscc'],
        stdout=subprocess.DEVNULL,   # redirect stdout
        stderr=subprocess.DEVNULL,   # redirect stderr
        stdin=subprocess.DEVNULL     # optional, avoids "ignoring input"
    )
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
              vprint(f"Waiting {int(secs)} seconds...", flush=True)
      except subprocess.CalledProcessError:
          print("GXSCC window not found.")
      time.sleep(0.5)
      secs += 0.5
      if secs > 20:
        print("GXSCC took too long. Exiting.", flush=True)
        subprocess.call(['pkill', '-f', 'gxscc.exe'])
        sys.exit(1)
  subprocess.call(['kdotool', 'windowminimize', f'{uuid}'])

  # Set up ctrl+c handler
  
  def signal_handler(sig, frame):
    print('Quitting...', flush=True)
    subprocess.call(['pkill', '-f', 'wine.*gxscc.exe'])
    sys.exit(0)
  
  signal.signal(signal.SIGINT, signal_handler)

  # Tell the user how many midi files are found, mainly for debug reasons
  print(f"Found {len(midi_files)} MIDI files in the directory: {directory}", flush=True)

  # Shuffle the list if wanted
  if args.shuffle:
    vprint("Shuffling midi files", flush=True)
    random.shuffle(midi_files)
  
  vprint("Generating lengths for MIDI files...", flush=True)
  # Store lengths in array
  midi_lengths = generate_lengths(midi_files)
  vprint("Lengths generated for MIDI files.", flush=True)

  # This is the part the user will actually be able to see
  print("------------------------", flush=True)
  print("Starting playback... \n Press Ctrl+C to stop.", flush=True)
  
  # Open midi file, play it, wait, repeat
  while True:
    for midi_file, length in midi_lengths:
      if length is not None:
        wine_path = "Z:" + midi_file.replace("/", "\\")
        subprocess.Popen(
            ['nohup', 'gxscc', wine_path],
            env={**os.environ, 'WINEDEBUG': '-all'},
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        print(flush=True)
        print(f"Playing {os.path.basename(midi_file)} for {round(length)} seconds...", flush=True)
        # Wait for the midi file to finish playing
        time.sleep(length)
      else:
        # Say if a midi file was skipped
        print(f"Skipping {os.path.basename(midi_file)} due to length being None.", flush=True)
    if not loop:
      print("Finished playing all MIDI files. Exiting.", flush=True)
      subprocess.call(['pkill', '-f', 'wine.*gxscc.exe'])
      break
    print("Finished! Looping...", flush=True)


# Not necessary, who would want to import this?
if __name__ == '__main__':
  main()

