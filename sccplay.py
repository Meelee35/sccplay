# Probably the most dependencies used in one of my projects 

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
import pygetwindow as gw

# Cheers cGPT. Only time its been used so dont complain.
def get_midi_files(directory):
    p = Path(directory)
    return [str(f) for f in p.iterdir() if f.is_file() and f.suffix.lower() in ['.mid', '.midi']]

# Get the length of the midi file, skip type 2
def get_midi_length_seconds(midi_file):
    mid = mido.MidiFile(midi_file)
    try:
        return mid.length
    except ValueError:
        print(f"Cannot get length for asynchronous (type 2) MIDI: {midi_file}")
        return None

# Assign length to each file so we know when to start the next song. I don't think theres an official way to detect when gxscc finishes a track
def generate_lengths(midi_files):
    lengths = []
    for midi_file in midi_files:
        try:
            length = get_midi_length_seconds(midi_file)
            lengths.append((midi_file, length))
            print(f"{os.path.basename(midi_file)}: {length} seconds")
        except Exception as e:
            print(f"Error processing {midi_file}: {e}")
    return lengths


def main():
  # Self explanatory
  parser = argparse.ArgumentParser(description='Play a playlist of midi files in GXSCC.')
  parser.add_argument('-d', '--dir', help='Optional: Midi Directory', default='')
  parser.add_argument('-s', '--shuffle', help='Optional: Shuffle Midi files', action='store_true')
  parser.add_argument('-l,', '--loop', help='Optional: Loop Midi files', action='store_true')
  args = parser.parse_args()
  
  # Edge case: gxscc not in path
  if shutil.which('gxscc') is None:
    print("GXSCC was not found in the PATH.")
    sys.exit(1)

  # did you specify a directory?
  if args.dir == '':
    directory = os.getcwd()
  else:
    directory = args.dir
  
  # Was throwing errors using args.loop further down
  loop = args.loop

  # Also self explanatory
  midi_files = get_midi_files(directory)
  if not midi_files:
    print("No MIDI files found in the specified directory.")
    return

  # Some logging
  print(f"Found {len(midi_files)} MIDI files in the directory: {directory}")

  # Shuffle 
  if args.shuffle:
    random.shuffle(midi_files)
  
  # More logging and also generate the length array
  print("Generating lengths for MIDI files...")
  midi_lengths = generate_lengths(midi_files)
  print("Lengths generated for MIDI files.")

  # Oooh.. pretty!
  print("------------------------")
  print("Starting playback...")
  
  # Welcome to the jank zone
  while True:
    for midi_file, length in midi_lengths:
      if length is not None:
        # I originally used this variable, i had planned to use it with the kill function but it didn't work and I never removed it.
        proc = subprocess.Popen(['cmd', '/c', 'start', '/min', 'gxscc', midi_file], shell=True)
        print()
        print(f"Playing {os.path.basename(midi_file)} for {round(length)} seconds...")
        
        def signal_handler(sig, frame):
          print('Quitting...')
          subprocess.call(['taskkill', '/F', '/IM', 'gxscc.exe'])
          sys.exit(0)
          
        time.sleep(0.2)
        
        # For some reason /min only works the next time its opened, as i was originally killing gxscc each time i wanted to play a new song. Figured out i dont need that.
        for win in gw.getWindowsWithTitle('GASHISOFT GXSCC'):
          win.minimize()
          break

        # Take a look at this nice ctrl+c handling
        signal.signal(signal.SIGINT, signal_handler)
        time.sleep(length-0.2)
      else:
        # How much logging does one need?
        print(f"Skipping {os.path.basename(midi_file)} due to length being None.")
    if not loop:
      print("Finished playing all MIDI files. Exiting.")
      subprocess.call(['taskkill', '/F', '/IM', 'gxscc.exe'])
      break
    print("Finished! Looping...")



if __name__ == '__main__':
  main()


# Phew! That was a lot. What nerd even reads all the code anyway?!