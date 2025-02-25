import grpc
from src.generated import recipe_index_pb2
from src.generated import recipe_index_pb2_grpc

recipe = {
    "id": '123456-uuid',
    "title": "Example Recipe",
    "instructions": "Mix ingredients and bake at 350 degrees.",
    "notes": "Use organic ingredients for better taste.",
    "is_public": True
}

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = recipe_index_pb2_grpc.RecipeSearchServiceStub(channel)
        response = stub.IndexRecipe(
            recipe_index_pb2.IndexRecipeRequest(
                id=recipe['id'],
                title=recipe['title'],
                instructions=recipe['instructions'],
                notes=recipe['notes'],
                is_public=recipe['is_public']
        ))
        print("Received from server:", response)

if __name__ == "__main__":
    run()
