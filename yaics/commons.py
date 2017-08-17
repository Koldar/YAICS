import socketserver
import struct

class Packet:

        PACKET_QUESTION = 0
        PACKET_ANSWER_OK = 1
        PACKET_ANSWER_KO = 2

        def __init__(self, magic_number, type, length, payload):
                self.magic_number = magic_number
                self.payload = payload
                self.type = type
                if length != len(payload):
                        raise ValueError("can't create a malformed packet")

        def __len__(self):
                return len(self.payload)

        @classmethod
        def create_answer(clazz, success):
                type = PACKET_ANSWER_OK if success else PACKET_ANSWER_KO
                return Packet(b'beefly', type, 0, b"")

        def __bytes__(self):
                length = struct.pack("<L", len(self.payload))
                type = struct.pack("c", self.type)
                return b"".join([self.magic_number, type, length, self.payload])

        @classmethod
        def parse(clazz, bytes_received):
                #magic number
                magic_number = bytes[0:6]
                if magic_number != b'beefly':
                        raise TypeError("this is not a packet we can handle")

                #type
                type = struct.unpack("c", bytes[6])[0]
                if type not in [PACKET_QUESTION, PACKET_ANSWER]:
                        raise TypeError("Unrecognized type")

                #length
                length = struct.unpack("<L", bytes[7:11])[0]

                #payload
                payload = bytes[11:length]

                return Packet(magic_number, type, length, payload)
