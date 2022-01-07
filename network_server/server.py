from network_client.config import Configuration
from network_common.wrappers import Request,Response
import socket
class NetworkServer:
    def __init__(self,request_handler):
        self.request_handler=request_handler
        self.server_configuration=Configuration()
        self.server_configuration.validate_values()
        if self.server_configuration.has_exceptions==True:
            for exception in self.server_configuration.exceptions.values():
                print(exception[1])
                sys.exit()
    def start(self):
        server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server_socket.bind(("localhost",self.server_configuration.port))
        server_socket.listen()
        while True:
            print(f"Server is ready to accept at port {self.server_configuration.port}")
            client_socket,client_socket_name=server_socket.accept()
            data_bytes=b''
            to_recieve=1024
            while len(data_bytes)<to_recieve:
                data_bytes+=client_socket.recv(to_recieve-len(data_bytes))
            request_data_length=int(data_bytes.decode("utf-8").strip())
            data_bytes=b''
            to_recieve=request_data_length
            while len(data_bytes)<to_recieve:
                data_bytes+=client_socket.recv(to_recieve-len(data_bytes))
            request_data=data_bytes.decode("utf-8")
            request=Request.from_json(request_data)
            response=self.request_handler(request)
            response_data=response.to_json()
            print(type(response_data))
            client_socket.sendall(bytes(str(len(response_data)).ljust(1024),"utf-8"))
            client_socket.sendall(bytes(response_data,"utf-8"))
            client_socket.close()
            
        