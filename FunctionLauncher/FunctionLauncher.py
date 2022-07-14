# encoding: utf-8
import socket
import struct

from FunctionLauncher.JsonObjectEncoder import JsonObjectEncoder


class FunctionLauncher:

    def __init__(self, host: str, port: int):
        self.instance = None
        self.instance_class = None
        self.instance_function = None
        self.instance_function_args = None
        self.instance_function_kwargs = None
        self.returned_instance = None
        self.function_return = None

        self._host = host
        self._port = port

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self._host, self._port))

    def __call__(self, function):
        self.instance_function = function

        def launcher(*args, **kwargs):
            self.instance = args[0]
            self.instance_class = args[0].__class__
            self.instance_function_args = args[1:]
            self.instance_function_kwargs = kwargs
            return self.run()

        return launcher

    #####################################################################

    def send(self):
        json_dumps = JsonObjectEncoder.dumps(self.to_representation())
        json_bytes = struct.pack('>I', len(json_dumps)) + bytearray(json_dumps, "utf-8")
        self._socket.sendall(json_bytes)

    def receive(self):
        json_bytes_length = self.receive_all(4)
        if not json_bytes_length:
            return None
        json_dumps_length = struct.unpack('>I', json_bytes_length)[0]
        return self.receive_all(json_dumps_length)

    def receive_all(self, message_length):
        data = bytearray()
        while len(data) < message_length:
            packet = self._socket.recv(message_length - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data

    #####################################################################

    def to_representation(self):
        return {
            "instance": self.instance,
            "class": self.instance_class.__name__,
            "function": self.instance_function.__name__,
            "args": self.instance_function_args,
            "kwargs": self.instance_function_kwargs
        }

    #####################################################################

    def run(self):
        self.send()
        data = self.receive()
        returned_dict = JsonObjectEncoder.loads(data.decode("utf-8"))
        self.returned_instance = returned_dict["instance"]
        self.function_return = returned_dict["return"]
        self.instance.__dict__ = self.returned_instance.__dict__
        return self.function_return
