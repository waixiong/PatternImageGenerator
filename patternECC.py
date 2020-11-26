import math
from reedsolo import RSCodec, ReedSolomonError

errorPercent = 0.4

def encodeWithReedSolo(bytedata):
    rsc = RSCodec(math.ceil(len(bytedata)*errorPercent))
    encodedata = rsc.encode(bytedata)
    return encodedata

def decodeWithReedSolo(encodedata):
    ecc_len = math.ceil(len(encodedata) / (1+errorPercent) * errorPercent)
    rsc = RSCodec(math.ceil(ecc_len))

    check = rsc.check(encodedata)
    try:
        decoded_msg, decoded_msgecc, errata_pos = rsc.decode(encodedata)
        check = rsc.check(decoded_msgecc)
        return decoded_msg, check, len(errata_pos)
    except:
        return b'', check, ecc_len // 2 + 1

# example
# data = b'0123456789ABCDEF0123456789ABCDEF01'
# edata = encodeWithReedSolo(data)
# print(len(edata))
# edata = b'0123456789ABCDEF0123456789ABCDEF01\x0e\xe4O[b\xbd\x1e\xd7[\x02\xd6\xacJ\x80'
# msg, check, errorlen = decodeWithReedSolo(edata)
# print(msg)
# print(check)
# print(errorlen)