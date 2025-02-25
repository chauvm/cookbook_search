import grpc
from src.generated import search_pb2
from src.generated import search_pb2_grpc
from src.generated import recipe_search_service_pb2
from src.generated import recipe_search_service_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        search_stub = search_pb2_grpc.PingPongStub(channel)
        search_response = search_stub.Ping(search_pb2.PingRequest(message="Hello, Server!"))
        print("Received from server:", search_response.message)
        recipe_stub = recipe_search_service_pb2_grpc.RecipeSearchServiceStub(channel)  # Correct stub
        
        recipe_response = recipe_stub.SearchRecipes(recipe_search_service_pb2.SearchRequest())  # Ensure method exists
        print("Received from server:", recipe_response.results)

if __name__ == "__main__":
    run()
