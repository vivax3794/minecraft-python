import socket
import struct
import typing as t

from . import utils


class Client():
    def __init__(self):
        self.connection = socket.socket()
        self.compression_on = False
        self.data = bytearray()

    def send_packet(self, id_: int, data: bytearray) -> None:
        pack = utils.write_var_int(id_) + data
        print("sending packet of lenght: ", len(pack))
        pack = utils.write_var_int(len(pack)) + pack
        print("sending:", pack)
        self.connection.sendall(pack)

    def read_packet(self) -> t.Tuple[int, bytearray]:
        self.data += self.connection.recv(1024)
        lenght = utils.read_var_int(self.data)
        pack = self.data[:lenght]
        self.data = self.data[lenght:]

        id_ = utils.read_var_int(pack)
        return id_, pack

    def login(self, username: str, ip: str, port: int = 25565) -> None:
        print("connecting to server:", ip)
        self.connection.connect((ip, port))

        # hansake
        print("sending hansake")
        self.send_packet(
                0x00,
                utils.write_var_int(754) +
                utils.write_string(ip) +
                struct.pack("H", port) +
                utils.write_var_int(2)
                )

        # login start
        print("sending login start")
        self.send_packet(
                0x00,
                utils.write_string(username)
                )

        print("waiting on server")
        id_, pack = self.read_packet()
        if id_ == 0x03:
            raise ValueError("Compression not supported yet.")

        elif id_ == 0x02:
            # Succes!
            print("we did it!")
        else:
            print("got packet of id: ", hex(id_), "with data: ", struct.unpack(f"{len(pack)}s", pack))
