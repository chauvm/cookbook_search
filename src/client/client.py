import grpc
from src.generated import search_pb2
from src.generated import search_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = search_pb2_grpc.PingPongStub(channel)
        response = stub.Ping(search_pb2.PingRequest(message="Hello, Server!"))
        print("Received from server:", response.message)

if __name__ == "__main__":
    run()
