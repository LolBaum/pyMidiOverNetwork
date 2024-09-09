import rtmidi
from rtmidi.randomout import RandomOut
from time import sleep
from Networking.server import Server
import logging
import traceback


def midi_from_string(string):
    content = string.split(",")
    if len(content) != 3:
        logging.error("message length has wrong format, msg=" + string)
    midi_type = content[0]

    midi_value = int(content[1])
    midi_channel = int(content[2])

    midi = None

    if midi_type == "ON":
        midi = rtmidi.MidiMessage.noteOn(1, midi_value, midi_channel)
    elif midi_type == "OFF":
        midi = rtmidi.MidiMessage.noteOff(1, midi_value)
    elif midi_type == "CONTROLLER":
        midi = rtmidi.MidiMessage.controllerEvent(1, midi_value, midi_channel)
    else:
        logging.error(f"message type ({midi_type}) not recognized: msg={string}")

    return midi


class MidiOutServer:
    def __init__(self, portName):
        self.server = Server(ip="10.10.5.49", callback=self.handle_message)

        # Name of the MIDI port in use
        self.portName = portName

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

        self.server.start()

    def send_message(self, msg):
        self.midiOut.sendMessage(msg)

    def handle_message(self, msg):
        try:
            msg_list = msg.split(';')
            for m in msg_list:
                if m == '':
                    continue
                print(m)
                m_midi = midi_from_string(m)
                print(m_midi)
                self.send_message(m_midi)
        except ValueError as e:
            logging.error(
                f"Could not parse message: {msg}\n{traceback.format_exc()}"
            )





    def cleanup(self):
        del self.midiOut




out = MidiOutServer("loopMIDI Port")

out.start()

# TODO: messages for velocity
# TODO: improve protocol to support stream of messages (msg0;msg1;msg2...)
# TODO: add local config for ip + port




