import rtmidi
from time import sleep
from Networking.client import Client

def print_message(midi):
    print(midi)
    if midi.isNoteOn():
        print('ON: ', midi.getMidiNoteName(midi.getNoteNumber()), midi.getVelocity())
    elif midi.isNoteOff():
        print('OFF:', midi.getMidiNoteName(midi.getNoteNumber()))
    elif midi.isController():
        print('CONTROLLER', midi.getControllerNumber(), midi.getControllerValue())
    print()


class MidiIn:
    def __init__(self):
        self.client = Client()
        self.midiin = rtmidi.RtMidiIn()
        self.ports = range(self.midiin.getPortCount())

    def run(self):
        self.client.start()
        self.ports = range(self.midiin.getPortCount())
        if self.ports:
            for i in self.ports:
                print(self.midiin.getPortName(i))
            print("Opening port 0!")
            self.midiin.openPort(0)
            while True:
                m = self.midiin.getMessage(250)  # some timeout in ms
                if m:
                    self.handle_message(m)
        else:
            print('NO MIDI INPUT PORTS!')

    def handle_message(self, msg):
        print_message(msg)
        self.client.send(msg)


MidiIn().run()



