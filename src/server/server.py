import logging
import grpc
from concurrent import futures
from src.generated.recipe_index_pb2_grpc import RecipeSearchServiceServicer, add_RecipeSearchServiceServicer_to_server
from src.generated.recipe_index_pb2 import IndexRecipeResponse, IndexRecipeRequest
from src.server.elasticsearch_client import ElasticsearchClient
# from src.generated.search_pb2 import PongResponse
# from src.generated.search_pb2_grpc import PingPongServicer, add_PingPongServicer_to_server

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

class RecipeIndexService(RecipeSearchServiceServicer):
    def __init__(self):
        super().__init__()
        self.es_client = ElasticsearchClient()

    def IndexRecipe(self, request, context):
        logger.info(f"Indexing recipe: {request}")
        try:
            # Index the recipe in Elasticsearch
            recipe = {
                "id": request.id,
                "title": request.title,
                "instructions": request.instructions,
                "notes": request.notes,
                "isPublic": request.is_public
            }
            self.es_client.index_recipe(recipe=recipe)
            logger.info(f"Recipe indexed successfully.")
            return IndexRecipeResponse(success=True)
        except Exception as e:
            logger.error(f"Error indexing recipe: {e}")
            return IndexRecipeResponse(success=False, error_message=str(e))

class SearchServer:
    def __init__(self, port):
        self.port = port
        self.server = None

    def start(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        add_RecipeSearchServiceServicer_to_server(RecipeIndexService(), self.server)
        self.server.add_insecure_port(f'[::]:{self.port}')
        self.server.start()
        print(f"Server started on port {self.port}")
        self.server.wait_for_termination()

    def stop(self):
        if self.server:
            self.server.stop(0)
