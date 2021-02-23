import mido

def getMenufacturer():
    return '00 21 10'

def getDeviceID():
    return '08'

def getChecksum(command):
    cmd = [int(x, 16) for x in command.split()]
    sum = len(cmd)
    for i in cmd:
        sum = (sum * 3 + i) & 0xff
    sum = sum & 0x7f
    return '{:02X}'.format(sum)

def createSysEx(cmd):
    return 'F0 {} 77 {} {} {} F7'.format(getMenufacturer(), getDeviceID(), cmd, getChecksum(cmd))

def sendSysEx(device, command):
    outport = mido.open_output(device)
    print(createSysEx(command))
    msg = mido.Message.from_hex(createSysEx(command))
    outport.send(msg)


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

def setScale(scale, device):
    sendSysEx(device, scaleCommands[scale])
    


    
#inport = mido.open_input('2- LUMI Keys Block 0')

setScale('blues', '2- LUMI Keys Block 1')

#print(mido.get_output_names())


