import grpc
from concurrent import futures
from src.generated.search_pb2 import PongResponse
from src.generated.search_pb2_grpc import PingPongServicer, add_PingPongServicer_to_server

class PingPongService(PingPongServicer):
    def Ping(self, request, context):
        return PongResponse(message=f"Pong: {request.message}")

class SearchServer:
    def __init__(self, port):
        self.port = port
        self.server = None

    def start(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        add_PingPongServicer_to_server(PingPongService(), self.server)
        self.server.add_insecure_port(f'[::]:{self.port}')
        self.server.start()
        print(f"Server started on port {self.port}")
        self.server.wait_for_termination()

    def stop(self):
        if self.server:
            self.server.stop(0)
