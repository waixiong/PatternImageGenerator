import math
import os
from reedsolo import RSCodec, ReedSolomonError

errorPercent = 0.4

def checkAbleWithReedSolo(length, byteData):
    ecc_len = math.ceil(len(byteData) / (1+errorPercent) * errorPercent)
    return ecc_len <= length

def estimateLengthWithReedSolo(byteData):
    ecc_len = math.ceil(len(byteData)*errorPercent)
    return len(byteData) + ecc_len

def encodeWithReedSolo(bytedata, length = 0):
    if len(bytedata) > 182 or length > 256:
        return b''
    ecc_len = 0
    if length == 0:
        # if len(bytedata) > 182:
        #     c = math.ceil(len(bytedata) / 2)
        #     if c > 182: 
        #         c = 182
        #     return encodeWithReedSolo(bytedata[:c]) + encodeWithReedSolo(bytedata[c:])
        ecc_len = math.ceil(len(bytedata)*errorPercent)
    else:
        # if length > 255:
        #     c = math.ceil(length / 2)
        #     print(c)
        #     if c > 255: 
        #         c = 255
        #     return encodeWithReedSolo(bytedata[:c]) + encodeWithReedSolo(bytedata[c:])
        print('use length '+str(length))
        ecc_len = math.ceil(int(length) / (1+errorPercent) * errorPercent)
        bytedata += os.urandom(math.floor(length - ecc_len - len(bytedata)))
    print('error: '+str(ecc_len))
    print('random: '+str(math.floor(length - ecc_len - len(bytedata))))
    print('data: '+str(len(bytedata)))
    rsc = RSCodec(ecc_len)
    encodedata = rsc.encode(bytedata)
    print('ENCODED')
    print(len(encodedata))
    return encodedata

def decodeWithReedSolo(encodedata):
    if len(encodedata) > 255:
        return b'', False, 255
    # print(encodedata)
    # if len(encodedata) > 255:
    #     c = math.ceil(len(encodedata) / 2)
    #     print(c)
    #     if c > 255: 
    #         c = 255
    #     byte2, check2, err2 = decodeWithReedSolo(encodedata[c:])
    #     byte1, check1, err1 = decodeWithReedSolo(encodedata[:c])
    #     if (check2[0] and check1[0]):
    #         print(check2)
    #         return byte1 + byte2, check1, err1 + err2
    #     else:
    #         ecc_len = math.ceil(len(encodedata) / (1+errorPercent) * errorPercent)
    #         return b'', False, ecc_len // 2 + 1
    ecc_len = math.ceil(len(encodedata) / (1+errorPercent) * errorPercent)
    # print(ecc_len)
    rsc = RSCodec(math.ceil(ecc_len))

    check = rsc.check(encodedata)
    try:
        decoded_msg, decoded_msgecc, errata_pos = rsc.decode(encodedata)
        check = rsc.check(decoded_msgecc)
        return decoded_msg, check, len(errata_pos)
    except:
        return b'', check, ecc_len // 2 + 1

def checkEOF(bytesData):
    counter = 0
    index = 0
    for byte in bytesData:
        if byte == 0x1a:
            counter += 1
            break
        else:
            index += 1
    return bytesData[:index]

# example
data = b'01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901'
edata = encodeWithReedSolo(data)
print(edata)
print(len(edata))
# edata = b'01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901\xd2\xebw\xee\x9e sRT\xda:0D\x99\xe3\xcf>\xea\x8f\xf1^a;}\xeb+L\xa1\x12\xfe\x1cs\x1c\xb9\xbcLb2345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012c\xeb\x9b:\xe2w\x1a\xa3\xb7dhp!\xec4\xa6\xff\xea\xdf\xd8,\x1d\x15q\x93L\x88ck\xe3\x96R\xfb\xe2\xb3\x1b,'
# msg, check, errorlen = decodeWithReedSolo(edata)
# print(msg)
# print(check)
# print(errorlen)

# data = b'TheChee\x1a\xf8\x7f\x9a\x92a\xe1\x84\x80\xd0\\\xa3\x04\x1c\\\xfb%T7\x0f9b\xb5s\x99\xa27\x1eO2Fw\xb3\xc8\xe8\xa5\x98\x842\x1f\xaf\n<\xba\xe1k\x963@q\xe7\xff\xc6P\x8e\x81\xe6\x8f\xa9\x91\x93\x9c\xcd\xd1\xe3P\xe9'
# d = checkEOF(data)
# print(d)
# print(len(d))