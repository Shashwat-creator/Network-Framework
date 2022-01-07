from network_client.config import Configuration
from network_common.wrappers import Request,Response
import socket
class NetworkClient:
    def __init__(self):
        self.server_configuration=Configuration()
        self.server_configuration.validate_values()
        if self.server_configuration.has_exceptions==True:
            for exception in self.server_configuration.exceptions.values():
                print(exception[1])
                sys.exit()
    def send(self,request):
        client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client_socket.connect((self.server_configuration.host,self.server_configuration.port))
        request_data=request.to_json()
        client_socket.sendall(bytes(str(len(request_data)).ljust(1024),"utf-8"))
        client_socket.sendall(bytes(request_data,"utf-8"))
        data_bytes=b''
        to_recieve=1024
        while len(data_bytes)<to_recieve:
            data_bytes+=client_socket.recv(to_recieve-len(data_bytes))
        response_data_length=int(data_bytes.decode("utf-8").strip())
        data_bytes=b''
        to_recieve=response_data_length
        while len(data_bytes)<to_recieve:
            data_bytes+=client_socket.recv(to_recieve-len(data_bytes))
        response_data=data_bytes.decode("utf-8")
        client_socket.shutdown(socket.SHUT_RDWR)
        client_socket.close()
        response=Response.from_json(response_data)
        return response
        
        
        