print(r"""
  ____          _____     _   _       _       
 / ___| ___ _ _|_   _|   | \ | | ___ | |_ ___ 
| |  _ / _ \ '_ \| |_____|  \| |/ _ \| __/ _ \
| |_| |  __/ | | | |_____| |\  | (_) | ||  __/
 \____|\___|_| |_|_|     |_| \_|\___/ \__\___|
                                              
""")


import numpy as np
import sounddevice as sd
import time
import random
import csv
import sys

# Define the 12-note scale (C, C#, D, D#, E, F, F#, G, G#, A, A#, B)
NOTES = [
    ('S', 261.63), ('r', 277.18), ('R', 293.66), ('g', 311.13), ('G', 329.63),
    ('m', 349.23), ('M', 369.99), ('P', 392.00), ('d', 415.30), ('D', 440.0),
    ('n', 466.16), ('N', 493.88)
]

# Generate scales: Lower (1 octave down), Mid, Upper (1 octave up)
LOWER_SCALE = [(f'.{name}', freq / 2) for name, freq in NOTES]
MID_SCALE = [(name, freq) for name, freq in NOTES]
UPPER_SCALE = [(f'{name}.', freq * 2) for name, freq in NOTES]
bias=2.0
SCALES = [LOWER_SCALE, MID_SCALE, UPPER_SCALE]

# Sound generation parameters
DURATION = 0.5  # seconds
SAMPLE_RATE = 44100  # samples per second

def generate_sine_wave(freq, duration, sample_rate):
    """Generate a sine wave for a given frequency and duration."""
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = 0.5 * np.sin(2 * np.pi * freq * t)
    return wave

# Read Transition Probability Matrix (TPM)
def readMatrix(file_path):
    tpm = []
    with open(file_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            tpm.append([float(value) for value in row])
    return tpm

def validate_starting_note():
    print("Available notes: S(1), r(2), R(3), g(4), G(5), m(6), M(7), P(8), d(9), D(10), n(11), N(12)")
    while True:
        try:
            user_input = input("Enter the starting note (1-12, corresponding to the above notes): ")
            note = int(user_input) - 1
            if 0 <= note <= 11:
                return note
            else:
                print("Invalid note. Please choose another note.")
        except ValueError:
            print("Please enter a valid number between 1 and 12.")

def generate_notes_from_tpm(starting_note):
    current_octave = 1  # Start in mid octave
    note = starting_note
    notes = [(note, current_octave)]
    
    for _ in range(50):
        random_number = random.random()
        next_note = note
        
        # Check if the next note should be in the mid octave (octave 1)
        if current_octave == 1:
            # Increase probability of staying in the mid octave
            biased_tpm = [tpm[note][j] * bias if j == note else tpm[note][j] for j in range(12)]
        else:
            biased_tpm = tpm[note]

        # Normalize the biased TPM to ensure it sums to 1
        total = sum(biased_tpm)
        biased_tpm = [value / total for value in biased_tpm]
        
        # Select the next note based on the biased probabilities
        for j in range(12):
            if random_number <= sum(biased_tpm[:j+1]):
                next_note = j
                break
        
        # Check octave transition rules
        if note >= 8 and next_note <= 4:
            current_octave = min(current_octave + 1, 2)  # Move to upper octave
        elif note <= 4 and next_note >= 8:
            current_octave = max(current_octave - 1, 0)  # Move to lower octave
        
        # Boundary condition for octave
        if current_octave > 2:
            current_octave = 2
        if current_octave < 0:
            current_octave = 0
        
        notes.append((next_note, current_octave))
        note = next_note
    
    return notes

def play_notes():
    starting_note = validate_starting_note()
    
    # Play initial C note for 1.5 seconds
    print('Playing S (C) for 1.5 seconds')
    initial_wave = generate_sine_wave(261.63, 1.5, SAMPLE_RATE)
    sd.play(initial_wave, samplerate=SAMPLE_RATE)
    sd.wait()
    time.sleep(0.1)
    
    notes = generate_notes_from_tpm(starting_note)
    for note, octave in notes:
        note_name, freq = SCALES[octave][note]
        print(f'Playing {note_name} ({freq:.2f} Hz) in octave {octave}')
        wave = generate_sine_wave(freq, DURATION, SAMPLE_RATE)
        sd.play(wave, samplerate=SAMPLE_RATE)
        sd.wait()
        time.sleep(0.1)  # Small gap between notes

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <TPM.csv>")
        sys.exit(1)
    
    tpm = readMatrix(sys.argv[1])
    convertedTPM = [[0] * 12 for _ in range(12)]
    for i in range(12):
        s = 0
        for j in range(12):
            s += tpm[i][j]
            convertedTPM[i][j] = s
    
    play_notes()

