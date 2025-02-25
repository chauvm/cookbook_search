import logging
import grpc
from concurrent import futures
from src.server.elasticsearch_client import ElasticsearchClient

from grpc_reflection.v1alpha import reflection
from src.generated import search_pb2, search_pb2_grpc, recipe_search_service_pb2, recipe_search_service_pb2_grpc

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


class PingPongService(search_pb2_grpc.PingPongServicer):
    """
    Service for handling ping-pong requests.
    """

    def Ping(self, request, context):
        """
        Handles a ping request and returns a pong response.
        
        Args:
            request: The ping request.
            context: The gRPC context.
        
        Returns:
            A pong response.
        """
        return search_pb2.PongResponse(message=f"Pong: if I change here Ping should Change {request.message}")

class RecipeSearchService(recipe_search_service_pb2_grpc.RecipeSearchServiceServicer):
    """
    Service for handling search recipe
    """
    def __init__(self):
        # Initialize Elasticsearch client
        self.es_client = ElasticsearchClient()

    def SearchRecipes(self, request, context):
        """
        Handles a search request and returns a SearchResponse.

        Args:
            request: The search request.
            context: The gRPC context.

        Returns:
            A Search Response that are list of recipes.
        """

        # Extract parameters from request
        query_type = request.query_type  # match, match_phrase, term, etc.
        field = request.field  # Field to search in
        value = request.value  # Search term
        fields = list(request.fields) if request.fields else None  # Multi_match fields
        range_filter = {request.range_filter: {"gte": request.range_gte, "lte": request.range_lte}} if request.range_filter else None
        sort = [{"field": s.field, "order": s.order} for s in request.sort] if request.sort else None

        try:
            # Perform Elasticsearch search
            response = self.es_client.search_recipe(
                query_type=query_type,
                field=field,
                value=value,
                fields=fields,
                range_filter=range_filter,
                sort=sort,

            )

            # Build gRPC response
            search_results = []
            for hit in response["hits"]["hits"]:
                search_results.append(
                    recipe_search_service_pb2.Recipe(
                        id=hit["_id"],
                        title=hit["_source"].get("title", ""),
                        instructions=hit["_source"].get("instructions", "")
                    )
                )

            return recipe_search_service_pb2.SearchResponse(recipes=search_results)

        except Exception as e:
            logger.error(f"Error while searching recipes: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Error fetching search results from Elasticsearch")
            return recipe_search_service_pb2.SearchResponse()


class SearchServer:
    """
    A gRPC server for handling search requests.
    """

    def __init__(self, port):
        """
        Initializes the search server.
        
        Args:
            port: The port to listen on.
        """
        self.port = port
        self.server = None
    
    def start(self):
        """
        Starts the search server.
        """
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        search_pb2_grpc.add_PingPongServicer_to_server(PingPongService(), self.server)
        recipe_search_service_pb2_grpc.add_RecipeSearchServiceServicer_to_server(RecipeSearchService(), self.server)

        # Register both service descriptors for reflection
        SERVICE_NAMES = (
            search_pb2.DESCRIPTOR.services_by_name['PingPong'].full_name,
            recipe_search_service_pb2.DESCRIPTOR.services_by_name['RecipeSearchService'].full_name,
            reflection.SERVICE_NAME,
        )
        reflection.enable_server_reflection(SERVICE_NAMES, self.server)

        self.server.add_insecure_port(f"[::]:{self.port}")
        self.server.start()
        print(f"Server started on port {self.port}")
        self.server.wait_for_termination()


    def stop(self):
        """
        Stops the search server.
        """
        if self.server:
            self.server.stop(0)