# Do not touch these imports! They might topple like dominoes!
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

# Cheers chatGPT. Only time its been used so dont complain.
def get_midi_files(directory):
    p = Path(directory)
    return [str(f) for f in p.iterdir() if f.is_file() and f.suffix.lower() in ['.mid', '.midi']]

# Get the length of the midi file in seconds. We don't talk about type 2 midi files, to put it simply: they're weird.
def get_midi_length_seconds(midi_file):
    mid = mido.MidiFile(midi_file)
    try:
        return mid.length
    except ValueError:
        print(f"Cannot get length for asynchronous (type 2) MIDI: {midi_file}")
        return None

# Generate lengths for every midi file in the list. If a genie appeared I would wish for the ability to detect when gxscc finishes playing.
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
  # Can my code stop arguing?
  parser = argparse.ArgumentParser(description='Play a playlist of midi files in GXSCC.')
  parser.add_argument('-d', '--dir', help='Optional: Midi Directory', default='')
  parser.add_argument('-s', '--shuffle', help='Optional: Shuffle Midi files', action='store_true')
  parser.add_argument('-l', '--loop', help='Optional: Loop Midi files', action='store_true')
  args = parser.parse_args()
  
  # Edge case: gxscc not in path. Help!
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

  # Where are my midi files?
  midi_files = get_midi_files(directory)
  if not midi_files:
    # There are no midi files!
    print("No MIDI files found in the specified directory.")
    return

  # We do like some logging, so lets log how many midi files we found and in what directory.
  print(f"Found {len(midi_files)} MIDI files in the directory: {directory}")

  # This shuffles better than the card dealer at the casino, but only if you want it to.
  if args.shuffle:
    random.shuffle(midi_files)
  
  # We tell the user what we do, although it goes so fast you can't see it!
  print("Generating lengths for MIDI files...")
  # Generate isn't really the right word, maybe scan? We scan the midi files for their lengths.
  midi_lengths = generate_lengths(midi_files)
  print("Lengths generated for MIDI files.")

  # Distinct separation from the debug logging above. Gives the logs some space to breathe.
  print("------------------------")
  print("Starting playback... \n Press Ctrl+C to stop.")
  
  # Take a look at this nice ctrl+c handling. Could probably go in a museum.      
  def signal_handler(sig, frame):
    print('Quitting...')
    subprocess.call(['taskkill', '/F', '/IM', 'gxscc.exe'])
    sys.exit(0)
  
  signal.signal(signal.SIGINT, signal_handler)
  
  # Welcome to the jank zone. Have a terrible time here!
  # Anyway, it loops through the midi files, plays them, waits, then plays the next one.
  while True:
    for midi_file, length in midi_lengths:
      if length is not None:
        # I don't think i need to run subprocess like this but it does work.
        proc = subprocess.Popen(['cmd', '/c', 'start', '/min', 'gxscc', midi_file], shell=True)
        print()
        print(f"Playing {os.path.basename(midi_file)} for {round(length)} seconds...")
        
        # Give gxscc a moment. He's old now. Let me know if it doesn't minimise.
        time.sleep(0.5)
        
        # For some reason /min only works the next time its opened, as i was originally killing gxscc each time i wanted to play a new song. Figured out i dont need that.
        for win in gw.getWindowsWithTitle('GASHISOFT GXSCC'):
          win.minimize()
          break

        time.sleep(length-0.5)
      else:
        # How much logging does one need? This is getting ridiculous.
        print(f"Skipping {os.path.basename(midi_file)} due to length being None.")
    if not loop:
      print("Finished playing all MIDI files. Exiting.")
      subprocess.call(['taskkill', '/F', '/IM', 'gxscc.exe'])
      break
    print("Finished! Looping...")


# I really don't think this is necessary but some dude might want to import this!
if __name__ == '__main__':
  main()


# Phew! That was a lot. What nerd even reads all the code anyway?!
