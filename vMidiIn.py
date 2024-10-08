import rtmidi
from time import sleep
from Networking.client import Client
import logging
from config import get_server_ip

def print_message(midi):
    print(midi)
    print(midi_to_string)
    print()

def midi_to_string(midi):
    s = ""
    if midi.isNoteOn():
        s = f'ON,{midi.getNoteNumber()},{midi.getVelocity()}'
    elif midi.isNoteOff():
        s = f'OFF,{midi.getNoteNumber()},0'
    elif midi.isController():
        s = f'CONTROLLER,{midi.getControllerNumber()},{midi.getControllerValue()}'
    else:
        raise logging.error("failed to convert midi to string. Message Type not implemented: msg=" + str(midi))
    return s


class MidiIn:
    def __init__(self, midi_port=0):
        self.client = Client(get_server_ip())
        self.midiin = rtmidi.RtMidiIn()
        self.ports = range(self.midiin.getPortCount())
        self.midiPort = midi_port

    def run(self):
        self.client.start()
        self.ports = range(self.midiin.getPortCount())
        if self.ports:
            for i in self.ports:
                print(self.midiin.getPortName(i))
            print("Opening port 0!")
            self.midiin.openPort(self.midiPort)
            while True:
                m = self.midiin.getMessage(250)  # some timeout in ms
                if m:
                    self.handle_message(m)
        else:
            print('NO MIDI INPUT PORTS!')

    def handle_message(self, msg):
        msg_str = midi_to_string(msg) + ';'
        print_message(msg_str)
        self.client.send(msg_str)


if __name__ == '__main__':
    MidiIn(1).run()
