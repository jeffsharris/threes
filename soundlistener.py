"""
PyAudio Example: Make a wire between input and output (i.e., record a
few samples and play them back immediately).

This is the callback (non-blocking) version.
"""

import pyaudio
import audioop
import time
import threescompanion
import termios, fcntl, sys, os # used for reading key input from terminal

WIDTH = 2
CHANNELS = 2
RATE = 44100

class SoundListener:
    def __init__(self, game):
        self.game = game
        self.soundLength = 0
        self.moveCount = 0
        self.prevSoundValue = 0
        self.peakReached = False
        self.timeSinceSilence = 0
        self.timeSinceLastMove = 0
        
        self.p = pyaudio.PyAudio()
        
        self.fd = sys.stdin.fileno()

        self.oldterm = termios.tcgetattr(self.fd)
        self.newattr = termios.tcgetattr(self.fd)
        self.newattr[3] = self.newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(self.fd, termios.TCSANOW, self.newattr)

        self.oldflags = fcntl.fcntl(self.fd, fcntl.F_GETFL)
        fcntl.fcntl(self.fd, fcntl.F_SETFL, self.oldflags | os.O_NONBLOCK)

    def moveCheck(self, data):
        if (data < 300) & (self.timeSinceSilence < 13) & (self.timeSinceSilence > 6) & (self.timeSinceLastMove > 15):
            self.moveCount += 1
            self.timeSinceLastMove = 0
            print "******* Move " + str(self.moveCount) + " detected"
            self.game.processIncrement()
            print "Done"


    def findAudioChannel(self):
        for i in range(0, self.p.get_device_count()):
            if self.p.get_device_info_by_index(i)["name"] == "Soundflower (2ch)":
                print "Channel " + str(i)
                return i
        return None

    def listenCallback(self, in_data, frame_count, time_info, status):
        data = audioop.rms(in_data, 2)
        #if (data == 0 & (self.timeSinceLastMove == 0)) | (data > 0):
            #print str(data) + "  " + str(self.peakReached) + " " + str(self.timeSinceSilence)
        if data > self.prevSoundValue:
            self.timeSinceSilence += 1
            if self.peakReached:
                self.peakReached = False
                self.moveCheck(data)
        
        if data < self.prevSoundValue:
            self.timeSinceSilence += 1
            if not self.peakReached:
                self.peakReached = True
    
        if (data == 0):
            self.moveCheck(self.prevSoundValue)
            self.timeSinceSilence = 0
            self.peakReached = False
    
        self.timeSinceLastMove += 1
        self.prevSoundValue = data
        return (in_data, pyaudio.paContinue)


    def listen(self):
        channel = self.findAudioChannel()
        stream = self.p.open(format=self.p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=False,
                input_device_index=channel,
                stream_callback=self.listenCallback)
        

        stream.start_stream()

        try:
            while stream.is_active():
                self.tryToFindKey()
                time.sleep(0.1)
        finally:
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.oldterm)
            fcntl.fcntl(self.fd, fcntl.F_SETFL, self.oldflags)

        stream.stop_stream()
        stream.close()
        
    def close(self):
        self.p.terminate()
        
    def tryToFindKey(self):
        try:
            c = sys.stdin.read(1)
            self.game.processKey(repr(c))
        except IOError: pass
        
def start(game):
    listener = SoundListener(game)
    listener.listen()   