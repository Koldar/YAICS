import socketserver
import simple.rpc.server

if __name__ == "__main__" 
        HOST, PORT = "localhost", 9999

        #create the server
        server = simple.rpc.server.SimpleRPCServer((HOST, PORT), simple.rpc.server.CommandHandler)
        server.serve_forever()

