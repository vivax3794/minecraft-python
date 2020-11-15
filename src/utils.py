import struct
import typing as t


class Identifier:
    def __init__(self, namespace: str, thing: str) -> None:
        self.namespace = namespace
        self.thing = thing


def read_var_int(stream: bytearray) -> int:
    num_read = 0
    result = 0
    while True:
        byte = stream.pop(0)
        value = byte & 0b01111111
        result |= value << (7 * num_read)
        num_read += 1

        if num_read > 5:
            raise ValueError("var int to long.")
        if byte & 0b10000000 == 0:
            break

    return struct.unpack("i", struct.pack("I", result))[0]


def read_var_long(stream: bytearray) -> int:
    num_read = 0
    result = 0
    while True:
        byte = stream.pop(0)
        value = byte & 0b01111111
        result |= value << (7 * num_read)
        num_read += 1

        if num_read > 10:
            raise ValueError("var long to long.")
        if byte & 0b10000000 == 0:
            break

    return struct.unpack("l", struct.pack("L", result))[0]


def write_var_int(value: int) -> bytearray:
    result = bytearray()
    while True:
        temp = value & 0b01111111
        value >>= 7
        if value != 0:
            temp |= 0b10000000

        result += struct.pack("B", temp)

        if value == 0:
            break

    return result


def write_var_long(value: int) -> bytearray:
    result = bytearray()
    while True:
        temp = value & 0b01111111
        value >>= 7
        if value != 0:
            temp |= 0b10000000

        result += struct.pack("B", temp)

        if value == 0:
            break

    return result


def read_string(stream: bytearray) -> t.Tuple[str, bytearray]:
    length = read_var_int(stream)
    data = stream[:length].decode()
    stream = stream[length:]
    return data, stream


def write_string(s: str) -> bytearray:
    data = s.encode()
    return write_var_int(len(data)) + data
