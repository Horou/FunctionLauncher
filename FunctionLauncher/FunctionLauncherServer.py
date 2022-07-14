import socket
import struct
from FunctionLauncher.JsonObjectEncoder import JsonObjectEncoder


class FunctionLauncherServer():
    def __init__(self, host: str, port: int):

        self._host = host
        self._port = port

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind((self._host, self._port))
        self._socket.listen(2)

    #####################################################################

    @staticmethod
    def send(connection, return_dict):
        json_dumps = JsonObjectEncoder.dumps(return_dict)
        json_bytes = struct.pack('>I', len(json_dumps)) + bytearray(json_dumps, "utf-8")
        connection.sendall(json_bytes)

    @staticmethod
    def receive(connection):

        def receive_all(connection, data_length):
            data = bytearray()
            while len(data) < data_length:
                packet = connection.recv(data_length - len(data))
                if not packet:
                    return None
                data.extend(packet)
            return data

        bytes_length = receive_all(connection, 4)
        if not bytes_length:
            return None
        data_length = struct.unpack('>I', bytes_length)[0]
        return receive_all(connection, data_length)

    #####################################################################

    @staticmethod
    def get_function_result(instance, function_name, function_args, function_kwargs):
        result = getattr(instance, function_name)(*function_args, **function_kwargs)
        return {
            "instance": instance,
            "return": result
        }

    @staticmethod
    def extract_data(json_bytes):
        data_dict = JsonObjectEncoder.loads(json_bytes.decode("utf-8"))
        return data_dict["instance"], data_dict["function"], data_dict["args"], data_dict["kwargs"]

    #####################################################################

    def run(self):
        while True:
            print("Listening on port: "+str(self._port))
            connection, socket_address = self._socket.accept()
            connection.settimeout(2.0)
            print("Connected to %s" % str(socket_address))
            try:
                while True:
                    self.handle(connection)
            except:
                pass

    def handle(self, connection):
        print("Listening on port: " + str(self._port))
        json_bytes = self.receive(connection)
        instance, function_name, args, kwargs = self.extract_data(json_bytes)
        print("Data Received:\n%s" % str((instance, function_name, args, kwargs)))
        result = self.get_function_result(instance, function_name, args, kwargs)
        print("instance: %s\nreturn: %s" % (result["instance"], result["return"]))
        self.send(connection, result)
