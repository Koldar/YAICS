
import socketserver
from yaics import server_utils
import argparse

if __name__ == "__main__":
        parser = argparse.ArgumentParser()
        parser.add_argument('-i', "--ip",
                type=str,
                required=False,
                default="0.0.0.0",
                help="The IP we need to listen on"
        )
        parser.add_argument('-p', "--port",
                type=int,
                required=False,
                default=9999,
                help="The port we need to listen on"
        )

        args = parser.parse_args()

        HOST = args.ip
        PORT = args.port

        #create the server
        server = server_utils.SimpleRPCServer((HOST, PORT), server_utils.CommandHandler)
        print("created server on {}:{}. Now I will wait endlessly for new connections. Kill me when you are done!".format(HOST, PORT))
        try:
                server.serve_forever()
        except KeyboardInterrupt:
                pass
        finally:
                print("Exiting")


