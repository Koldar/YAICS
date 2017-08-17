from socketserver import ThreadingMixIn
from socketserver import TCPServer
from socketserver import BaseRequestHandler
from subprocess import check_call
from subprocess import CalledProcessError
import struct
import socket
import os
from yaics.commons import Packet
from yaics.commons import ParseError

class SimpleRPCServer(ThreadingMixIn, TCPServer):
	pass

class CommandHandler(BaseRequestHandler):
	
	def execute_payload(self, packet):
		cmd = packet.payload.decode("utf-8")
		cmds = cmd.split(" ")

		try:
			cwd = os.getcwd()
			print("executing \"{}\" inside \"{}\"".format(cmd, cwd))
			check_call(cmds)
			print("DONE")
		except CalledProcessError as e:
			print("NOT DONE")
			return e.returncode
		return 0

	def fetch_packet(self):
		total_bytes = b""
		packet = None
		while True:
			bytes_received = self.request.recv(1024)
			if bytes_received is None:
				success = False
				break
			if len(bytes_received) == 0:
				success = False
				break

			print("arrived {}".format(bytes_received))
			total_bytes = b"".join([total_bytes, bytes_received])
			print("the whole data is {}".format(total_bytes))
			try:
				packet = Packet.parse(total_bytes, "utf-8")
			except ParseError as e:
				print(str(e))
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
		except Exception as e:
			reply = Packet.create_answer(False, str(e))
		finally:
			self.request.sendall(reply.encode())
