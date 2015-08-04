import pyaudio
import time
import wave

sound = None

def playCallback(in_data, frame_count, time_info, status):
    global sound
    data = sound.readframes(frame_count)
    return (data, pyaudio.paContinue)    

def playSound():
    global sound
    CHUNK = 1024
        
    p = pyaudio.PyAudio()
        
    sound = wave.open('Ping.wav', 'rb')
    
        
        
    stream = p.open(format=p.get_format_from_width(sound.getsampwidth()),
        channels=sound.getnchannels(),
        rate=sound.getframerate(),
        output_device_index=2,
        output=True,
        stream_callback=playCallback)

    stream.start_stream()

    while stream.is_active():
        time.sleep(0.1)

    stream.stop_stream()
    stream.close()
    sound.close()