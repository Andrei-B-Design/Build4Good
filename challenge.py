#By Andrei Bugayong
import sys
#!{sys.executable} --version
#!{sys.executable} -m ensurepip --default-pip
#!{sys.executable} -m pip --version
#!{sys.executable} -m pip install pyaudio
#!{sys.executable} -m pip install pvcobra

import pyaudio
import wave
import pvcobra
import numpy as np
import os


############# Variables and Key #############
chunk = 512  # Record in chunks of 512 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 16000  # Record at 16000 samples per second
seconds = 5 # records in 5 second intervals
spacer = 0 # to prevent immediate recording
n=5 # to document length of recording
frames = [] # for the audio recording
access_key = '26XZ9QrIhNPBCIC4jphMIKumQiQ/phM3rAo2M/3M7QX1ji7//7j5LA=='
cobra = pvcobra.create(access_key)
#############################################


############# Microphone defined #############
p = pyaudio.PyAudio()

stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                input=True,
                frames_per_buffer = chunk)
##############################################


############# check for audio #############
under_value = 0
over_value = 0
def get_next_audio_frame():
    audio_data = stream.read(chunk,False)
    audio_frame = np.frombuffer(audio_data, dtype=np.int16)
    return audio_frame

while True:
    audio_frame=get_next_audio_frame()
    voice_probability = cobra.process(audio_frame)
    voice_probability_float = float(voice_probability)
    if voice_probability_float < 0.014:
        under_value += 1
        over_value = 0
    if spacer > 20:
        if voice_probability_float > 0.014:
            under_value = 0
            over_value += 1
    spacer += 1
###########################################


############# record audio #############
    if over_value == 15:
        print("Audio detected: Recording")
        audio_file = (f'{n}_seconds.wav')
        for i in range(0, int(fs / chunk * seconds)):
            data = stream.read(chunk)
            frames.append(data)
        wf = wave.open(audio_file, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()
        over_value = 0
        if n != 5:
            os.remove(f'{n-5}_seconds.wav')
        print("Finished Recording")
        print("Total seconds recorded so far:",n)
        n+=5
########################################        
            
stream.stop_stream()
stream.close()
p.terminate()