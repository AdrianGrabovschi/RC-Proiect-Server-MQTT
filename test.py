
def getPacketRemainingLength(data):
    multiplier = 1
    value = 0
    index = 2
    while True:
        byte = data[index]
        value += (byte & 127) * multiplier
        if not(byte & 128):
            break
        multiplier = multiplier * 128
        index += 1
    return index - 1, value

getPacketRemainingLength(b'\x00\xFF\xFF\x77')