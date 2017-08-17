from socketserver import ThreadingMixIn
from socketserver import TCPServer
from socketserver import BaseRequestHandler
from subprocess import call
import struct
from yaics.commons import Packet

class SimpleRPCServer(ThreadingMixIn, TCPServer):
	pass

class CommandHandler(BaseRequestHandler):
	
	def execute_payload(self, packet):
		cmd = str(packet.payload)
		cmds = cmd.split(" ")

		try:
			check_call(cmds)
		except CallProcessError as e:
			return e.returncode
		return 0

	def fetch_packet(self):
		total_bytes = b""
		packet = None
		socket.settimeout()
		while True:
			bytes_received = self.request.recv(1024)
			if bytes_received is None:
				success = False
				break
			if len(bytes_received) == 0:
				success = False
				break

			total_bytes = b"".join([total_bytes, bytes_received])
			try:
				packet = Packet.parse(total_bytes)
			except Exception:
				continue
			else:
				success = True
			break

		return (packet, success)

	def handle(self):
		try:
			packet, success = self.fetch_packet()
			if success:
				self.execute_payload(packet)
				reply = Packet.create_answer(True)
			else:
				reply = Packet.create_answer(False)
		except TypeError:
			reply = Packet.create_answer(False)
		finally:
			self.request.sendall(bytes(reply))
