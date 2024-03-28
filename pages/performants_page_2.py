import streamlit as st
import time
import os
import numpy as np
from scipy.io import wavfile
import parselmouth
from parselmouth.praat import call
from IPython.display import Audio
import pyaudio
import wave
import sounddevice as sd
import soundfile as sf
assert numpy  # avoid "imported but unused" message (W0611)



def record(x):
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 44100  # Record at 44100 samples per second
    seconds = x
    filename = "output.wav"

    p = pyaudio.PyAudio()  # Create an interface to PortAudio


    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

# Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

# Stop and close the stream 
    stream.stop_stream()
    stream.close()
# Terminate the PortAudio interface
    p.terminate()

# Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    fs, x = wavfile.read("output.wav")

    return fs, x


def formants_praat(x, fs):
        
        f0min, f0max  = 75, 300
        sound = parselmouth.Sound(x, fs) # read the sound
        pitch = sound.to_pitch()
        f0 = pitch.selected_array['frequency']
        formants = sound.to_formant_burg(time_step=0.010, maximum_formant=5000)
        
        f1_list, f2_list  = [], []
        for t in formants.ts():
            f1 = formants.get_value_at_time(1, t)
            f2 = formants.get_value_at_time(2, t)
            if np.isnan(f1): f1 = 0
            if np.isnan(f2): f2 = 0
            f1_list.append(int(f1))
            f2_list.append(int(f2))
            
        return f0, f1_list, f2_list

def real_time_vowel(color):
    st.write(f":{color}[Begin with the unrounded vowel. When finished, break off the voice abruptly rather than letting it trail off.]")

    m = 5
    while m > 0:
        st.write(f":{color}[Begin in {m} seconds]")
        time.sleep(1)
        m -= 1

    st.write(f":{color}[GO!]")
    time.sleep(1)

    fs, x = record(.10)
    f0, f1, f2 = formants_praat(x, fs)

    f0_values = []
    f1_values = []
    f2_values = []
    while np.mean(f0) > 0:

        fs, z = record(.10)
        f0, f1, f2 = formants_praat(z, fs)

        col1, col2, col3 = st.columns(3)
        col1.metric(":green[F0]", int(np.mean(f0)))
        col2.metric(":red[F1]", int(np.mean(f1)))
        col3.metric(":blue[F2]", int(np.mean(f2)))
        f0_values.append(int(np.mean(f0)))
        f1_values.append(int(np.mean(f1)))
        f2_values.append(int(np.mean(f2)))

    f0_values.pop(-1)
    f1_values.pop(-1)
    f2_values.pop(-1)
    f0_values.sort()
    f1_values.sort()
    f2_values.sort()

    st.write(f"Your F1 for this vowel ranged from {f1_values[0]} to {f1_values[-1]}, for an average F1 of {int(np.mean(f1_values))}.") 
    st.write(f"Your F2 for this vowel ranged from {f2_values[0]} to {f2_values[-1]}, for an average F2 of {int(np.mean(f2_values))}.")

    return f0_values[0], f0_values[-1], int(np.mean(f0_values)), f1_values[0], f1_values[-1], int(np.mean(f1_values)), f2_values[0], f2_values[-1], int(np.mean(f2_values))



st.header("WELCOME TO THE PERFORMANTS PRACTICE PAGE!")

st.write("We will practice your French mixed vowels here. You know how your diction " +
         "teachers are always telling you these vowels need to be brighter? Well, here " +
         "is your chance to see what the numbers say. We'll look at these vowels in pairs. " +
         "You remember that [ i ] and [ y ] are pronounced in the same place, except that the lips are " +
         "rounded for [ y ]. Similarly, [ e ] and [ ø ] are pronounced in the same place, with the lips " +
         "rounded for [ ø ]. And the same situation holds for [ ɛ ] and [ œ ].")

st.write("For the purposes of this exercise, F1 values correspond to the relative " +
         "openness of the vowel. A lower F1 value corresponds to a more closed vowel. " +
         "F2 values correspond to relative backness of a vowel. A more forward vowel will " +
         "have a higher F2. You can also drop your F2 value by rounding your lips, which is " +
         "crucial for the French mixed vowels.")

st.write("For each pair of vowels, begin with the unrounded vowel, listed first. Sustain the vowel and " +
         "experiment with closing your mouth, raising your tongue, and brightening the vowel. See how these " +
         "manipulations affect your F1 and F2 values. Then move to the second vowel. Your F1 should stay about " +
         "the same (give or take 50 Hz). The F2 will drop significantly, but should not drop more than about 500 Hz.")

first_set = st.button(":red[Click here for [ i ] and [ y ].]")
second_set = st.button(":blue[Click here for [ e ] and [ ø ].]")
third_set = st.button(":green[Click here for [ ɛ ] and [ œ ].]")

colors = ["red", "blue", "green"]

if first_set:
    real_time_vowel("red")
   
elif second_set:
    real_time_vowel("blue")

elif third_set:
    real_time_vowel("green")

go_ahead = st.button("Click here when finished with the first vowel. You will probably need to scroll up.")

if go_ahead:
    real_time_vowel("black")
     
