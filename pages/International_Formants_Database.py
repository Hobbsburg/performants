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
import sys
import sounddevice as sd
import soundfile as sf
import pandas as pd
from datetime import date
from streamlit_gsheets import GSheetsConnection

@st.cache_data

def record(x, color):
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 44100  # Record at 44100 samples per second
    seconds = x
    filename = "output.wav"

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    secs = 5
    while secs > 1:
        st.write(f":{color}[Get ready! {secs} seconds]")
        time.sleep(1)  # Delay for 1 second
        secs -= 1
    st.write(f":{color}[Breathe in and...]")
    time.sleep(1)
    st.write(f':{color}[BEGIN RECORDING. Sustain the vowel until you see "Finished recording."]')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

# Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk, exception_on_overflow = False)
        frames.append(data)

# Stop and close the stream 
    stream.stop_stream()
    stream.close()
# Terminate the PortAudio interface
    p.terminate()

    st.write('Finished recording')

# Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    fs, x = wavfile.read("output.wav")
 #   Audio(x,rate=fs)
    return fs, x


def formants_praat(x, fs):
        
        f0min, f0max  = 75, 300
        sound = parselmouth.Sound(x, fs) # read the sound
        pitch = sound.to_pitch()
        f0 = pitch.selected_array['frequency']
        formants = sound.to_formant_burg(time_step=0.010, maximum_formant=5000)
        
        f1_list, f2_list, f3_list, f4_list, t_list  = [], [], [], [], []
        for t in formants.ts():
            f1 = formants.get_value_at_time(1, t)
            f2 = formants.get_value_at_time(2, t)
            if np.isnan(f1): f1 = 0
            if np.isnan(f2): f2 = 0
            f1_list.append(int(f1))
            f2_list.append(int(f2))
            t_list.append("{:.2f}".format(t))
            
        return f0, f1_list, f2_list,
   
def create_word_list(language, vowel_list, english_word_list):

    x = 0
    word_list = []
    while x < len(vowel_list):
        if english_word_list[x] != "-":
            temp_word = english_word_list[x].split(" ")
            english_word = temp_word[0]
        else:
            english_word = "[vowel not used in English]"
        sample_word = st.text_input(f"Is the vowel {vowel_list[x]} as in the English word '{english_word}' in your language? If YES, " +
                                    "please enter a word from your language transliterated into English IN CAPITAL LETTERS, preferably " +
                                    "beginning with [ b ], [ p ], [ m ] or nothing, with this vowel in the FIRST syllable. " +
                                    "If NO, please enter a single hypen ('-').")
        word_list.append(sample_word)
        x += 1
    return word_list
                    

conn = st.connection("gsheets", type=GSheetsConnection)
new_df = conn.read()
all_data = []
new_data = {}
usernames = []

z = 0
while z < 950:
    temp_data = {}
    username = new_df.loc[z][1]
    usernames.append(username)
    temp_date = new_df.loc[z][0]
    if str(temp_date)[0] == "2":
        temp_data["DATE"] = new_df.loc[z][0]
        temp_data["NAME"] = new_df.loc[z][1]
        temp_data["LANGUAGE"] = new_df.loc[z][2]
        temp_data["VOICE TYPE"] = new_df.loc[z][3]
        temp_data["VOWEL [ i ] F0"] = new_df.loc[z][4]
        temp_data["VOWEL [ i ] WORD"] = new_df.loc[z][5]
        temp_data["VOWEL [ i ] F1"] = new_df.loc[z][6]
        temp_data["VOWEL [ i ] F2"] = new_df.loc[z][7]
        temp_data["VOWEL [ ɪ ] F0"] = new_df.loc[z][8]
        temp_data["VOWEL [ ɪ ] WORD"] = new_df.loc[z][9]
        temp_data["VOWEL [ ɪ ] F1"] = new_df.loc[z][10]
        temp_data["VOWEL [ ɪ ] F2"] = new_df.loc[z][11]
        temp_data["VOWEL [ e ] F0"] = new_df.loc[z][12]
        temp_data["VOWEL [ e ] WORD"] = new_df.loc[z][13]
        temp_data["VOWEL [ e ] F1"] = new_df.loc[z][14]
        temp_data["VOWEL [ e ] F2"] = new_df.loc[z][15]
        temp_data["VOWEL [ ɛ ] F0"] = new_df.loc[z][16]
        temp_data["VOWEL [ ɛ ] WORD"] = new_df.loc[z][17]
        temp_data["VOWEL [ ɛ ] F1"] = new_df.loc[z][18]
        temp_data["VOWEL [ ɛ ] F2"] = new_df.loc[z][19]
        temp_data["VOWEL [ æ ] F0"] = new_df.loc[z][20]
        temp_data["VOWEL [ æ ] WORD"] = new_df.loc[z][21]
        temp_data["VOWEL [ æ ] F1"] = new_df.loc[z][22]
        temp_data["VOWEL [ æ ] F2"] = new_df.loc[z][23]
        temp_data["VOWEL [ a ] F0"] = new_df.loc[z][24]
        temp_data["VOWEL [ a ] WORD"] = new_df.loc[z][25]
        temp_data["VOWEL [ a ] F1"] = new_df.loc[z][26]
        temp_data["VOWEL [ a ] F2"] = new_df.loc[z][27]
        temp_data["VOWEL [ ɑ ] F0"] = new_df.loc[z][28]
        temp_data["VOWEL [ ɑ ] WORD"] = new_df.loc[z][29]
        temp_data["VOWEL [ ɑ ] F1"] = new_df.loc[z][30]
        temp_data["VOWEL [ ɑ ] F2"] = new_df.loc[z][31]
        temp_data["VOWEL [ ɨ ] F0"] = new_df.loc[z][32]
        temp_data["VOWEL [ ɨ ] WORD"] = new_df.loc[z][33]
        temp_data["VOWEL [ ɨ ] F1"] = new_df.loc[z][34]
        temp_data["VOWEL [ ɨ ] F2"] = new_df.loc[z][35]
        temp_data["VOWEL [ ə/ʌ/ɐ ] F0"] = new_df.loc[z][36]
        temp_data["VOWEL [ ə/ʌ/ɐ ] WORD"] = new_df.loc[z][37]
        temp_data["VOWEL [ ə/ʌ/ɐ ] F1"] = new_df.loc[z][38]
        temp_data["VOWEL [ ə/ʌ/ɐ ] F2"] = new_df.loc[z][39]
        temp_data["VOWEL [ ɔ ] F0"] = new_df.loc[z][40]
        temp_data["VOWEL [ ɔ ] WORD"] = new_df.loc[z][41]
        temp_data["VOWEL [ ɔ ] F1"] = new_df.loc[z][42]
        temp_data["VOWEL [ ɔ ] F2"] = new_df.loc[z][43]
        temp_data["VOWEL [ ɤ ] F0"] = new_df.loc[z][44]
        temp_data["VOWEL [ ɤ ] WORD"] = new_df.loc[z][45]
        temp_data["VOWEL [ ɤ ] F1"] = new_df.loc[z][46]
        temp_data["VOWEL [ ɤ ] F2"] = new_df.loc[z][47]
        temp_data["VOWEL [ o ] F0"] = new_df.loc[z][48]
        temp_data["VOWEL [ o ] WORD"] = new_df.loc[z][49]
        temp_data["VOWEL [ o ] F1"] = new_df.loc[z][50]
        temp_data["VOWEL [ o ] F2"] = new_df.loc[z][51]
        temp_data["VOWEL [ ʊ ] F0"] = new_df.loc[z][52]
        temp_data["VOWEL [ ʊ ] WORD"] = new_df.loc[z][53]
        temp_data["VOWEL [ ʊ ] F1"] = new_df.loc[z][54]
        temp_data["VOWEL [ ʊ ] F2"] = new_df.loc[z][55]
        temp_data["VOWEL [ u ] F0"] = new_df.loc[z][56]
        temp_data["VOWEL [ u ] WORD"] = new_df.loc[z][57]
        temp_data["VOWEL [ u ] F1"] = new_df.loc[z][58]
        temp_data["VOWEL [ u ] F2"] = new_df.loc[z][59]
        all_data.append(temp_data)
    z += 1

st.header("THE INTERNATIONAL FORMANTS DATABASE")

st.write("This exercise will measure your natural formants in your native language. " +
         "The data will be collected using a username chosen by you, and is available to view by clicking the link at the bottom of the page.")

name = st.text_input("Enter a username IN CAPITAL LETTERS. This will only be used by you if you would like to search for yourself on the database and see your formant values.")

if name in usernames:
    st.text_input("If this is your first time using this app, please select a different username. If this is not your first time, you may continue.")
                     
voice_type = st.selectbox("What is your voice type?", ["SOPRANO", "MEZZO", "ALTO", "COUNTERTENOR", "TENOR", "BARITONE", "BASS"])

language = st.selectbox("What is your native language? Select from the dropdown menu.", ["ENGLISH", "CHINESE", "RUSSIAN", "OTHER"])

vowel_list = [ "[ i ]", "[ ɪ ]", "[ e ]", "[ ɛ ]", "[ æ ]", "[ a ]", "[ ɑ ]", "[ ɨ ]", "[ ə/ʌ/ɐ ]", "[ ɔ ]", "[ ɤ ]", "[ o ]", "[ ʊ ]", "[ u ]"]

english_word_list = [ "BEE", "BIT", "BAY (sustain first vowel only)", "BET", "BAT", "POW (sustain first vowel only)", "POD", "-", "BUD", "BAWD",
                "-", "BOAT (sustain first vowel only)", "BOOK", "BOO" ]

#vowel_data_list = []

color_list = ["red", "blue", "green", "violet", "orange", "rainbow"]

if language == "ENGLISH":
    word_list = english_word_list
    
elif language == "CHINESE":
    word_list =  [ "逼 [bī]", "-","杯 [bēi]", "边 [biān]","-", "巴 [bā]", "-", "-", "很 [hěn]", "-", "和 [hé]", "拨 [bō]", "-", "扑 [pū]"]

elif language == "RUSSIAN":
    word_list = ["BIT' (БИТЬ)", "B'EDA (БЕДА) (sustain first vowel only)", "V'ERIT' (ВЕРИТЬ) (sustain first vowel only)", "B'ELYY (БЕЛЫЙ) (sustain first vowel only)",
                 "-", "BABUSHKA (БАБУШКА) (sustain first vowel only)", "BAL (БАЛ)", "BYL (БЫЛ)", "KHOROSHO (ХОРОШО) (sustain first vowel only)",
                 "BOL' (БОЛЬ)", "-", "-", "-", "BUD' (БУДЬ)"]

else:
    language = st.text_input("What is your language? Enter your answer in CAPITAL LETTERS.")
    word_list = create_word_list(language, vowel_list, english_word_list)
    
st.link_button(":red[Please read this document (2 pages) and click the 'I Agree' button below before continuing.]", "https://photos.app.goo.gl/X6Eir18WJ3zfF8qi7")
agree = st.checkbox("I agree")

#vowel_data_list = []
def update_dataframe(x):
    t = 0
    while t <= x:
        data = st.session_state[f"{vowel_list[t]}"]
        display_data = {}
        display_data["Date"] = date.today()
        display_data["Name"] = name
        display_data["Voice Type"] = voice_type
        display_data["Language"] = language
        display_data["Vowel"] = vowel_list[t]
        display_data["AVG F0"] = data[0]
        display_data["AVG F1"] = data[2]
        display_data["AVG F2"] = data[3]
        if data[0] != "-":
            vowel_data_list.append(display_data)
        t += 1
    df = pd.DataFrame(vowel_data_list)
    return df                      
    
if agree:
    st.write("WHEN PROMPTED, READ THE WORD YOU SEE AS NATURALLY AS POSSIBLE. HOWEVER, YOU ARE ASKED TO SUSTAIN THE VOWEL " +
             "FOR FIVE (5) SECONDS. IF THE WORD HAS MORE THAN ONE SYLLABLE, SUSTAIN THE VOWEL IN THE ***FIRST SYLLABLE*** ONLY. IF THE VOWEL IS PART OF A DIPHTHONG, " +
            "SUSTAIN THE ***FIRST VOWEL*** OF THE DIPHTHONG ONLY.")
    b = 0
    vowel_data_list = []
    while b < len(vowel_list):
        color = color_list[b % 6]
        if word_list[b] == "-":
            b+= 1
        else:
            st.write(f":{color}[VOWEL NO. {b+1}: ]", vowel_list[b])
            st.write(f":{color}[SAMPLE WORD: '{word_list[b]}']")
        
            go_ahead = st.button(f":{color}[Click here when ready to record {vowel_list[b]}. Scroll up if you don't see the prompt.]")
            if go_ahead:
                fs, x = record(5, color)
                f0, f1, f2 = formants_praat(x, fs)
                word = word_list[b].split(" ")
                col1, col2, col3 = st.columns(3)
                col1.metric(":red[F1]", int(np.mean(f1)))
                col2.metric(":blue[F2]", int(np.mean(f2)))
                col3.metric(":green[pitch]", int(np.mean(f0)))
                data = [int(np.mean(f0)), word[0], int(np.mean(f1)), int(np.mean(f2))]
                st.session_state[f"{vowel_list[b]}"] = data
           #     display_data = {}
           #     display_data["Date"] = date.today()
           #     display_data["Name"] = name
           #     display_data["Voice Type"] = voice_type
           #     display_data["Language"] = language
           #     display_data["Vowel"] = vowel_list[x]
           #     display_data["AVG F0"] = data[0]
           #     display_data["AVG F1"] = data[2]
           #     display_data["AVG F2"] = data[3]
           #     vowel_data_list.append(display_data)
                df = update_dataframe(b)
                st.write(df)           
                
            b += 1

#vowel_data_list = []

for vowel in vowel_list:
    if vowel not in st.session_state.keys():
        st.session_state[vowel] = ["-", "-", "-", "-"]

#x = 0

#while x < len(vowel_list):
 #   vowel_data = st.session_state[vowel_list[x]]
#    display_data = {}
  #  display_data["Date"] = date.today()
  #  display_data["Name"] = name
  #  display_data["Voice Type"] = voice_type
  #  display_data["Language"] = language
  #  display_data["Vowel"] = vowel_list[x]
  #  display_data["AVG F0"] = vowel_data[0]
  #  display_data["AVG F1"] = vowel_data[1]
  #  display_data["AVG F2"] = vowel_data[2]
  #  vowel_data_list.append(display_data)
  #  x += 1
#df = pd.DataFrame(vowel_data_list)
#st.dataframe(df)

    
final_data  = {}

final_data["DATE"] = date.today()
final_data["NAME"] = name
final_data["LANGUAGE"] = language
final_data["VOICE TYPE"] = voice_type
final_data["VOWEL [ i ] F0"] = st.session_state["[ i ]"][0]
final_data["VOWEL [ i ] WORD"] = st.session_state["[ i ]"][1]
final_data["VOWEL [ i ] F1"] = st.session_state["[ i ]"][2]
final_data["VOWEL [ i ] F2"] = st.session_state["[ i ]"][3]
final_data["VOWEL [ ɪ ] F0"] = st.session_state["[ ɪ ]"][0]
final_data["VOWEL [ ɪ ] WORD"] = st.session_state["[ ɪ ]"][1]
final_data["VOWEL [ ɪ ] F1"] = st.session_state["[ ɪ ]"][2]
final_data["VOWEL [ ɪ ] F2"] = st.session_state["[ ɪ ]"][3]
final_data["VOWEL [ e ] F0"] = st.session_state["[ e ]"][0]
final_data["VOWEL [ e ] WORD"] = st.session_state["[ e ]"][1]
final_data["VOWEL [ e ] F1"] = st.session_state["[ e ]"][2]
final_data["VOWEL [ e ] F2"] = st.session_state["[ e ]"][3]
final_data["VOWEL [ ɛ ] F0"] = st.session_state["[ ɛ ]"][0]
final_data["VOWEL [ ɛ ] WORD"] = st.session_state["[ ɛ ]"][1]
final_data["VOWEL [ ɛ ] F1"] = st.session_state["[ ɛ ]"][2]
final_data["VOWEL [ ɛ ] F2"] = st.session_state["[ ɛ ]"][3]
final_data["VOWEL [ æ ] F0"] = st.session_state["[ æ ]"][0]
final_data["VOWEL [ æ ] WORD"] = st.session_state["[ æ ]"][1]
final_data["VOWEL [ æ ] F1"] = st.session_state["[ æ ]"][2]
final_data["VOWEL [ æ ] F2"] = st.session_state["[ æ ]"][3]
final_data["VOWEL [ a ] F0"] = st.session_state["[ a ]"][0]
final_data["VOWEL [ a ] WORD"] = st.session_state["[ a ]"][1]
final_data["VOWEL [ a ] F1"] = st.session_state["[ a ]"][2]
final_data["VOWEL [ a ] F2"] = st.session_state["[ a ]"][3]
final_data["VOWEL [ ɑ ] F0"] = st.session_state["[ ɑ ]"][0]
final_data["VOWEL [ ɑ ] WORD"] = st.session_state["[ ɑ ]"][1]
final_data["VOWEL [ ɑ ] F1"] = st.session_state["[ ɑ ]"][2]
final_data["VOWEL [ ɑ ] F2"] = st.session_state["[ ɑ ]"][3]
final_data["VOWEL [ ɨ ] F0"] = st.session_state["[ ɨ ]"][0]
final_data["VOWEL [ ɨ ] WORD"] = st.session_state["[ ɨ ]"][1]
final_data["VOWEL [ ɨ ] F1"] = st.session_state["[ ɨ ]"][2]
final_data["VOWEL [ ɨ ] F2"] = st.session_state["[ ɨ ]"][3]
final_data["VOWEL [ ə/ʌ/ɐ ] F0"] = st.session_state["[ ə/ʌ/ɐ ]"][0]
final_data["VOWEL [ ə/ʌ/ɐ ] WORD"] = st.session_state["[ ə/ʌ/ɐ ]"][1]
final_data["VOWEL [ ə/ʌ/ɐ ] F1"] = st.session_state["[ ə/ʌ/ɐ ]"][2]
final_data["VOWEL [ ə/ʌ/ɐ ] F2"] = st.session_state["[ ə/ʌ/ɐ ]"][3]
final_data["VOWEL [ ɔ ] F0"] = st.session_state["[ ɔ ]"][0]
final_data["VOWEL [ ɔ ] WORD"] = st.session_state["[ ɔ ]"][1]
final_data["VOWEL [ ɔ ] F1"] = st.session_state["[ ɔ ]"][2]
final_data["VOWEL [ ɔ ] F2"] = st.session_state["[ ɔ ]"][3]
final_data["VOWEL [ ɤ ] F0"] = st.session_state["[ ɤ ]"][0]
final_data["VOWEL [ ɤ ] WORD"] = st.session_state["[ ɤ ]"][1]
final_data["VOWEL [ ɤ ] F1"] = st.session_state["[ ɤ ]"][2]
final_data["VOWEL [ ɤ ] F2"] = st.session_state["[ ɤ ]"][3]
final_data["VOWEL [ o ] F0"] = st.session_state["[ o ]"][0]
final_data["VOWEL [ o ] WORD"] = st.session_state["[ o ]"][1]
final_data["VOWEL [ o ] F1"] = st.session_state["[ o ]"][2]
final_data["VOWEL [ o ] F2"] = st.session_state["[ o ]"][3]
final_data["VOWEL [ ʊ ] F0"] = st.session_state["[ ʊ ]"][0]
final_data["VOWEL [ ʊ ] WORD"] = st.session_state["[ ʊ ]"][1]
final_data["VOWEL [ ʊ ] F1"] = st.session_state["[ ʊ ]"][2]
final_data["VOWEL [ ʊ ] F2"] = st.session_state["[ ʊ ]"][3]
final_data["VOWEL [ u ] F0"] = st.session_state["[ u ]"][0]
final_data["VOWEL [ u ] WORD"] = st.session_state["[ u ]"][1]
final_data["VOWEL [ u ] F1"] = st.session_state["[ u ]"][2]
final_data["VOWEL [ u ] F2"] = st.session_state["[ u ]"][3]
all_data.append(final_data)
 

update_button = st.button("Submit Formant Data")
if update_button:
    conn.update(data=all_data)

st.write("To see the database, please email me at performantsdata@gmail.com. I will send you a link.")

st.cache_data.clear()
            
