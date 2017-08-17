import socketserver
import struct

class ParseError(Exception):
	pass

class Packet:

        PACKET_QUESTION = 0
        PACKET_ANSWER_OK = 1
        PACKET_ANSWER_KO = 2

        def __init__(self, magic_number, packet_type, length, payload):
                self.magic_number = magic_number
                self.payload = payload
                self.type = packet_type
                if length != len(payload):
                        raise ValueError("can't create a malformed packet")

        def __len__(self):
                return len(self.payload)

        @classmethod
        def create_question(clazz, payload):
                if type(payload) is str:
	                b = bytes(payload, "utf-8")
                elif type(payload) is bytes:
                        b = payload
                else:
                        raise TypeError("can't encode payload!")

                return Packet(b'beefly', Packet.PACKET_QUESTION, len(b), b)

        @classmethod
        def create_answer(clazz, success, payload=None):
                packet_type = Packet.PACKET_ANSWER_OK if success else Packet.PACKET_ANSWER_KO
                if payload is None:
                        b = b""
                elif type(payload) is str:
                        b = bytes(payload, "utf-8")
                elif type(payload) is bytes:
                        b = payload
                else:
                        raise TypeError("can't encode payload")

                return Packet(b'beefly', packet_type, len(b), b)

        def encode(self, encoding="utf-8"):
                length = struct.pack("<L", len(self.payload))
                type = struct.pack("<L", self.type)
                return b"".join([self.magic_number, type, length, self.payload])

        @classmethod
        def parse(clazz, bytes_received, encoding="utf-8"):
                #magic number
                magic_number = bytes_received[0:6]
                if magic_number != b'beefly':
                        raise ParseError("this is not a packet we can handle")

                #type
                packet_type = struct.unpack("<L", bytes_received[6:10])[0]
                if packet_type not in [Packet.PACKET_QUESTION, Packet.PACKET_ANSWER_OK, Packet.PACKET_ANSWER_KO]:
                        raise ParseError("Unrecognized type")

                #length
                length = struct.unpack("<L", bytes_received[10:14])[0]

                #payload
                payload = bytes_received[14:14+length]

                retval = Packet(magic_number, packet_type, length, payload)
                return retval
