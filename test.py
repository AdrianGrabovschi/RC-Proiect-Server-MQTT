def encodePacketRemainingLength(X):
    ret = []
    while True:
        encodedByte = X % 128
        ret.append(encodedByte)
        X  = X // 128
        if X > 0:
            encodedByte = encodedByte | 128
        else:
            break
    return ret

ret = encodePacketRemainingLength(13)
print (ret)

print ('H%dsH%ds' % (len('asd'), len('dsa')))