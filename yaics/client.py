from commons import Packet
import socket
import sys
import argparse

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', "--ip",
		type=str,
		required=False,
		default="192.168.1.251"
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

	args = parser.parser_args()

	HOST = args.ip
	PORT = args.port
	data = args.command

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		#connect
		sock.connect((HOST, PORT))
		#receive
		sock.sendall(bytes(data, "utf-8"))
		#receive
		print("Sent message. We're now waiting for reply")
		received = str(sock.recv(1024), "utf-8")

		print("received" + received)
	finally:
		sock.close()

if __name__ == "__main__":
	main()
