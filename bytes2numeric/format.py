import struct

def bytes2numeric(bytes, format='f'):
    ba = bytearray(bytes)
    # return struct.unpack("!f",ba)[0] # 將 MSB 的 bytes 转成 float，用“!f”参数
    return struct.unpack(format,ba)[0] # 將 LSB bytes转成 float，用“f”参数

print(bytes2numeric([0, 0, 128, 63]))       # 默认float32
print(bytes2numeric([0, 0, 128, 63], 'i'))  # int32
print(bytes2numeric([0, 0, 128, 63], 'I'))  # unsigned int32
print(bytes2numeric([0, 0, 128, 63], 'I'))  # unsigned int32
