"""
PyAudio Example: Make a wire between input and output (i.e., record a
few samples and play them back immediately).

This is the callback (non-blocking) version.
"""

import pyaudio
import audioop
import time
import wave
import sys

WIDTH = 2
CHANNELS = 2
RATE = 44100

p = pyaudio.PyAudio()

soundLength = 0
moveCount = 0
prevSoundValue = 0
peakReached = False
timeSinceSilence = 0
timeSinceLastMove = 0

def playSound():
    CHUNK = 1024

    audio = wave.open('Ping.wav', 'rb')
    
    p = pyaudio.PyAudio()
    
    def playCallback(in_data, frame_count, time_info, status):
        data = audio.readframes(frame_count)
        return (data, pyaudio.paContinue)

    stream = p.open(format=p.get_format_from_width(audio.getsampwidth()),
                    channels=audio.getnchannels(),
                    rate=audio.getframerate(),
                    output_device_index=2,
                    output=True,
                    stream_callback=playCallback)

    stream.start_stream()

    while stream.is_active():
        time.sleep(0.1)

    stream.stop_stream()
    stream.close()
    audio.close()

    p.terminate()

def moveCheck(timeSinceSilence, data):
    global moveCount
    global timeSinceLastMove
    if (data < 300) & (timeSinceSilence < 13) & (timeSinceSilence > 6) & (timeSinceLastMove > 15):
        moveCount += 1
        timeSinceLastMove = 0
        print "******* Move " + str(moveCount) + " detected"
        playSound()

def callback(in_data, frame_count, time_info, status):
    global timeSinceSilence
    global prevSoundValue
    global peakReached
    global timeSinceLastMove
    
    data = audioop.rms(in_data, 2)
    if (data == 0 & (timeSinceLastMove == 0)) | (data > 0):
        print str(data) + "  " + str(peakReached) + " " + str(timeSinceSilence)
    if data > prevSoundValue:
        timeSinceSilence += 1
        if peakReached:
            peakReached = False
            moveCheck(timeSinceSilence, data)
        
    if data < prevSoundValue:
        timeSinceSilence += 1
        if not peakReached:
            peakReached = True
    
    if (data == 0):
        moveCheck(timeSinceSilence, prevSoundValue)
        timeSinceSilence = 0
        peakReached = False
    
    timeSinceLastMove += 1
    prevSoundValue = data
    return (in_data, pyaudio.paContinue)

stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=False,
                input_device_index=3,
                stream_callback=callback)

stream.start_stream()

while stream.is_active():
    time.sleep(0.1)

stream.stop_stream()
stream.close()

p.terminate()