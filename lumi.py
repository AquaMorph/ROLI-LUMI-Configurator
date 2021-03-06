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
        return 'F0 {} 77 {} {} {} F7'.format(self.getMenufacturer(),
                                             self.getDeviceID(),
                                             cmd,
                                             self.getChecksum(cmd))

    def sendSysEx(self, command):
        print(self.createSysEx(command))
        msg = mido.Message.from_hex(self.createSysEx(command))
        self.outport.send(msg)

    # MIDI Settings
    def setMIDIMode(self, mode):
        if mode.lower() == 'mpe':
            self.sendSysEx('10 20 20 00 00 00 00 00')
        elif mode.lower() == 'multi' or mode.lower() == 'multi channel':
            self.sendSysEx('10 20 00 00 00 00 00 00')
        elif mode.lower() == 'single' or mode.lower() == 'single channel':
            self.sendSysEx('10 20 40 00 00 00 00 00')
        return

    def setPitchBendRange(self, bendRange):
        # Error checking
        if (bendRange < 1 or bendRange > 96):
            print('ERROR: Pitch Bend Range of {} is not between 1 and 96'.format(bendRange))
            exit(1)
        one = (bendRange % 4) * 2
        two = '{:02X}'.format(int(bendRange / 4))
        self.sendSysEx('10 30 {}0 {} 00 00 00 00'.format(one, two))

    # MPE
    def setNoMIDIChannels(self, number):
        # Error checking
        if (number < 1 or number > 15):
            print('ERROR: No. MIDI Channels of {} is not between 1 and 15'.format(number))
            exit(1)
        one = (number % 4) * 2
        two = '{:02X}'.format(int(number / 4))
        self.sendSysEx('10 10 {}1 {} 00 00 00 00'.format(one, two))

    def setMPEZone(self, zone):
        if zone.lower() == 'lower' or zone.lower() == 'lower zone':
            self.sendSysEx('10 00 05 00 00 00 00 00')
        elif zone.lower() == 'upper' or zone.lower() == 'upper zone':
            self.sendSysEx('10 00 25 00 00 00 00 00')
        return

    # Multi Channel
    def setMIDIStartChannel(self, channel):
        # Error checking
        if (channel < 1 or channel > 16):
            print('ERROR: MIDI Start Channel of {} is not between 1 and 16'.format(channel))
            exit(1)
        one = (channel % 4) * 2
        two = '{:02X}'.format(int(channel / 4))
        self.sendSysEx('10 00 {}0 {} 00 00 00 00'.format(one, two))

    def setMIDIEndChannel(self, channel):
        # Error checking
        if (channel < 1 or channel > 16):
            print('ERROR: MIDI End Channel of {} is not between 1 and 16'.format(channel))
            exit(1)
        one = (channel % 4) * 2
        two = '{:02X}'.format(int(channel / 4))
        self.sendSysEx('10 10 {}0 {} 00 00 00 00'.format(one, two))

    # Single Channel
    def setMIDIChannel(self, channel):
        self.setMIDIStartChannel(channel)
        
    # Pitch
    def setOctive(self, octive):
        return

    def setTranspose(self, transpose):
        return

    # Sensitivity
    def setStrikeSensitivity(self, sensitivity):
        # Error checking
        if (sensitivity < 0 or sensitivity > 127):
            print('ERROR: Strike Sensitivity of {} is not between 1 and 127'.format(sensitivity))
            exit(1)
        one = (sensitivity % 4) * 2
        two = '{:02X}'.format(int(sensitivity / 4))
        self.sendSysEx('10 20 {}1 {} 00 00 00 00'.format(one, two))

    def setPressureSensitivity(self, sensitivity):
        # Error checking
        if (sensitivity < 0 or sensitivity > 127):
            print('ERROR: Pressure Sensitivity of {} is not between 1 and 127'.format(sensitivity))
            exit(1)
        one = (sensitivity % 4) * 2
        two = '{:02X}'.format(int(sensitivity / 4))
        self.sendSysEx('10 50 {}1 {} 00 00 00 00'.format(one, two))

    def setLiftSensitivity(self, sensitivity):
        # Error checking
        if (sensitivity < 0 or sensitivity > 127):
            print('ERROR: Lift Sensitivity of {} is not between 1 and 127'.format(sensitivity))
            exit(1)
        one = (sensitivity % 4) * 2
        two = '{:02X}'.format(int(sensitivity / 4))
        self.sendSysEx('10 60 {}1 {} 00 00 00 00'.format(one, two))

    def setFixedVelocity(self, fixed):
        if fixed:
            self.sendSysEx('10 70 21 00 00 00 00 00')
        else:
            self.sendSysEx('10 70 01 00 00 00 00 00')

    def setFixedVelocityValue(self, value):
        return

    # Keybed State
    def setActiveMode(self, mode):
        if mode == 1:
            self.sendSysEx('10 40 02 00 00 00 00 00')
        elif mode == 2:
            self.sendSysEx('10 40 22 00 00 00 00 00')
        elif mode == 3:
            self.sendSysEx('10 40 42 00 00 00 00 00')
        elif mode == 4:
            self.sendSysEx('10 40 62 00 00 00 00 00')

    scaleCommands = {
        'major':              '10 60 02 00 00 00 00 00',
        'minor':              '10 60 22 00 00 00 00 00',
        'harmonic minor':     '10 60 42 00 00 00 00 00',
        'chromatic':          '10 60 42 04 00 00 00 00',
        'pentatonic neutral': '10 60 62 00 00 00 00 00',
        'pentatonic major':   '10 60 02 01 00 00 00 00',
        'pentatonic minor':   '10 60 22 01 00 00 00 00',
        'blues':              '10 60 42 01 00 00 00 00',
        'dorian':             '10 60 62 01 00 00 00 00',
        'phrygian':           '10 60 02 02 00 00 00 00',
        'lydian':             '10 60 22 02 00 00 00 00',
        'mixolydian':         '10 60 42 02 00 00 00 00',
        'locrian':            '10 60 62 02 00 00 00 00',
        'whole tone':         '10 60 02 03 00 00 00 00',
        'arabic (a)':         '10 60 22 02 00 00 00 00',
        'arabic (b)':         '10 60 42 03 00 00 00 00',
        'japanese':           '10 60 62 03 00 00 00 00',
        'ryukyu':             '10 60 02 04 00 00 00 00',
        '8-tone spanish':     '10 60 22 04 00 00 00 00',
        'chromatic':          '10 60 42 04 00 00 00 00'
    }

    def setScale(self, scale):
        self.sendSysEx(self.scaleCommands[scale])

    keyCommands = {
        'c' : '10 30 03 00 00 00 00 00',
        'c#': '10 30 23 00 00 00 00 00',
        'd' : '10 30 43 00 00 00 00 00',
        'd#': '10 30 63 00 00 00 00 00',
        'e' : '10 30 03 01 00 00 00 00',
        'f' : '10 30 23 01 00 00 00 00',
        'f#': '10 30 43 01 00 00 00 00',
        'g' : '10 30 63 01 00 00 00 00',
        'g#': '10 30 03 02 00 00 00 00',
        'a' : '10 30 23 02 00 00 00 00',
        'a#': '10 30 43 02 00 00 00 00',
        'b' : '10 30 63 02 00 00 00 00'
    }

    def setKey(self, key):
        self.sendSysEx(self.keyCommands[key])

    def setPitchBendTracking(self, tracking):
        return

    def setPressureTracking(self, tracking):
        return

    # Colors
    def setGlobalKeyColor(self, color):
        self.sendSysEx('10 20 64 3F 00 7F 7F 03')

    def setRootKeyColor(self, color):
        self.sendSysEx('10 30 64 3F 00 00 7E 03')

    def setBrightness(self, brightness):
        one = (brightness % 4) * 2
        two = '{:02X}'.format(int(brightness / 4))
        self.sendSysEx('10 40 {}4 {} 00 00 00 00'.format(one, two))

    # Mode
    def setColorScheme(self, mode, scheme):

        # Mode error checking
        if (mode < 1 or mode > 4):
            print('ERROR: {} is not a valid mode'.format(mode))
            exit(1)

        # Converts name input
        if isinstance(scheme, str):
            scheme = scheme.lower()
            if scheme == 'pro':
                scheme = 0
            elif scheme == 'user':
                scheme = 1
            elif scheme == 'paino':
                scheme = 2
            elif scheme == 'stage':
                scheme = 3
            elif scheme == 'rainbow':
                scheme = 4
            else:
                print('ERROR: Unrecoginized color scheme {}'.format(scheme))
                exit(1)

        cmdOne = '{:X}'.format(5-mode)
        cmdTwo = '{:X}'.format(0xB+mode)
        one = (scheme % 4) * 2
        two = '{:02X}'.format(int(scheme / 4))
        self.sendSysEx('10 {}0 {}{} {} 00 00 00 00'.format(cmdOne, one, cmdTwo, two))
    
    def setEnablePitchBend(self, mode, enable):
        if enable:
            enable = 2
        else:
            enable = 0
        cmdOne = '{:X}'.format(7-mode)
        cmdTwo = '{:X}'.format(0xB+mode)
        self.sendSysEx('10 {}0 {}{} 00 00 00 00 00'.format(cmdOne, enable, cmdTwo))

    def setEnablePressure(self, mode, enable):
        if enable:
            enable = 2
        else:
            enable = 0
        cmdOne = '{:X}'.format(8-mode)
        cmdTwo = '{:X}'.format(0xB+mode)
        self.sendSysEx('10 {}0 {}{} 00 00 00 00 00'.format(cmdOne, enable, cmdTwo))

outputDevices = mido.get_output_names()
try:
    lumiOut = next(o for o in outputDevices if 'LUMI Keys' in o)
except:
    print('LUMI not detected')
    exit(1)

lumi = LUMI(lumiOut)
lumi.setScale('minor')
lumi.setMIDIMode('single')
lumi.setActiveMode(0)
lumi.setKey('c')
lumi.setFixedVelocity(False)
lumi.setGlobalKeyColor('#0BB5FF')
lumi.setRootKeyColor('#FFFFFF')
lumi.setBrightness(100)
lumi.setColorScheme(1, 1)
lumi.setColorScheme(2, 1)
lumi.setColorScheme(3, 'pro')
lumi.setColorScheme(4, 1)
lumi.setEnablePitchBend(1, True)
lumi.setEnablePitchBend(2, True)
lumi.setEnablePitchBend(3, True)
lumi.setEnablePitchBend(4, True)
lumi.setEnablePressure(1, True)
lumi.setEnablePressure(2, True)
lumi.setEnablePressure(3, True)
lumi.setEnablePressure(4, True)
lumi.setPitchBendRange(45)
lumi.setNoMIDIChannels(5)
lumi.setMPEZone('upper')
lumi.setMIDIStartChannel(1)
lumi.setMIDIEndChannel(16)
lumi.setMIDIChannel(16)
lumi.setStrikeSensitivity(63)
lumi.setPressureSensitivity(127)
lumi.setLiftSensitivity(127)
