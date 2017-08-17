from yaics.commons import Packet
import socket
import sys
import argparse

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', "--ip",
		type=str,
		required=False,
		default="192.168.1.251",
		help="The IP of the server to contact"
	)
	parser.add_argument('-p', "--port",
		type=int,
		required=False,
		default=9999,
		help="The port of the server to contact"
	)
	parser.add_argument('-c', "--command",
		type=str,
		required=True,
		help="The command to send to the server"
	)

	args = parser.parse_args()

	HOST = args.ip
	PORT = args.port
	data = args.command

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		#connect
		sock.connect((HOST, PORT))
		#receive
		pkt = Packet.create_question(data)
		sock.sendall(pkt.encode("utf-8"))
		#receive
		print("Sent message. We're now waiting for reply")
		received = sock.recv(1024)

		reply = Packet.parse(received, "utf-8")
		if reply.type == Packet.PACKET_ANSWER_OK:
			print("everything went fine")
		elif reply.type == Packet.PACKET_ANSWER_KO:
			print("Something went wrong")
			if len(reply.payload) > 0:
				print("-" * 20)
				print(reply.payload.decode("utf-8"))
				print("-" * 20)
		else:
			raise ValueError("reply type mismatch!")
	finally:
		sock.close()

if __name__ == "__main__":
	main()
