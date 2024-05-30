import rtmidi
from rtmidi.randomout import RandomOut
from time import sleep


# based on https://github.com/jaakkopee/neuronSeq nnmidiout.py
class MidiOut:
    def __init__(self):

        # Name of the MIDI port in use
        self.portName = "loopMIDI Port"

        self.midiOut = rtmidi.RtMidiOut()
        available_ports_count = self.midiOut.getPortCount()
        available_ports = [self.midiOut.getPortName(x) for x in range(available_ports_count)]
        print(f"{available_ports_count} available ports: {available_ports}")

        selected_index = available_ports.index(self.portName)
        print(f"selecting device {selected_index}: {self.midiOut.getPortName(selected_index)}")

        self.midiOut.openPort(selected_index)

        if self.midiOut.isPortOpen():
            print("successfully opened port")
        else:
            print("failed to open port")

    def send_message(self, msg):
        self.midiOut.sendMessage(msg)

    def cleanup(self):
        del self.midiOut


out = MidiOut()

rtmidi.MidiMessage()
out.send_message(rtmidi.MidiMessage.noteOn(1, 60, 100))
sleep(2)
out.send_message(rtmidi.MidiMessage.noteOff(1, 60))

# TODO: Client reading MIDI Input
# TODO: Client sending to server
# TODO: server receive msg
# TODO: Server send msg to MIDI Output

# TODO: messages for velocity




