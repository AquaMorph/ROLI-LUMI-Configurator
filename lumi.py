import mido

class LUMI:
    def __init__(self, device):
        self.outport = mido.open_output(device)
    
    def getMenufacturer(self):
        return '00 21 10'

    def getDeviceID(self):
        return '08'

    def getChecksum(self, command):
        cmd = [int(x, 16) for x in command.split()]
        sum = len(cmd)
        for i in cmd:
            sum = (sum * 3 + i) & 0xff
            sum = sum & 0x7f
        return '{:02X}'.format(sum)

    def createSysEx(self, cmd):
        return 'F0 {} 77 {} {} {} F7'.format(self.getMenufacturer(), self.getDeviceID(), cmd, self.getChecksum(cmd))

    def sendSysEx(self, command):
        print(self.createSysEx(command))
        msg = mido.Message.from_hex(self.createSysEx(command))
        self.outport.send(msg)

    # MIDI Settings
    def setMIDIMode(self, mode):
        return

    def setPitchBendRange(self, bendRange):
        return

    # MPE
    def setNoMIDIChannels(self, number):
        return

    def setMPEZone(self, zone):
        return

    # Multi Channel
    def setMIDIStartChannel(self, channel):
        return

    def setMIDIEndChannel(self, channel):
        return

    # Single Channel
    def setMIDIChannel(self, channel):
        return

    # Pitch
    def setOctive(self, octive):
        return

    def setTranspose(self, transpose):
        return

    # Sensitivity
    def setStrikeSensitivity(self, sensitivity):
        return

    def setPressireSensitivity(self, sensitivity):
        return

    def setLeftSensitivity(self, sensitivity):
        return

    def setFixedVelocity(self, fixed):
        return

    def setFixedVelocityValue(self, value):
        return

    # Keybed State
    def setActiveMode(self, mode):
        return

    scaleCommands = {
        'major': '10 60 02 00 00 00 00 00',
        'minor': '10 60 22 00 00 00 00 00',
        'harmonic minor': '10 60 42 00 00 00 00 00',
        'chromatic': '10 60 42 04 00 00 00 00',
        'pentatonic neutral': '10 60 62 00 00 00 00 00',
        'pentatonic major': '10 60 02 01 00 00 00 00',
        'pentatonic minor': '10 60 22 01 00 00 00 00',
        'blues': '10 60 42 01 00 00 00 00',
        'dorian': '10 60 62 01 00 00 00 00',
        'phrygian': '10 60 02 02 00 00 00 00',
        'lydian': '10 60 22 02 00 00 00 00',
        'mixolydian': '10 60 42 02 00 00 00 00',
        'locrian': '10 60 62 02 00 00 00 00',
        'whole tone': '10 60 02 03 00 00 00 00',
        'arabic (a)': '10 60 22 02 00 00 00 00',
        'arabic (b)': '10 60 42 03 00 00 00 00',
        'japanese': '10 60 62 03 00 00 00 00',
        'ryukyu': '10 60 02 04 00 00 00 00',
        '8-tone spanish': '10 60 22 04 00 00 00 00',
        'chromatic': '10 60 42 04 00 00 00 00'
    }

    def setScale(self, scale):
        self.sendSysEx(self.scaleCommands[scale])

    def setKey(self, key):
        return

    def setPitchBendTracking(self, tracking):
        return

    def setPressureTracking(self, tracking):
        return

    # Colors
    def setGlobalKeyColor(self, color):
        return

    def setRootKeyColor(self, color):
        return

    # Mode
    def setColorScheme(self, mode, scheme):
        return
    
    def setEnablePitchBend(self, mode, enable):
        return

    def setEnablePressure(self, mode, enable):
        return


lumi = LUMI('2- LUMI Keys Block 1')
lumi.setScale('minor')

