import unittest
import grpc
import threading
import time
from elasticsearch import Elasticsearch
from src.generated.recipe_index_pb2 import IndexRecipeRequest
from src.generated.recipe_index_pb2_grpc import RecipeSearchServiceStub
from src.server.server import SearchServer
from src.server.elasticsearch_client import ElasticsearchClient

ES_INDEX = "recipe"
TEST_RECIPE_ID = "test-recipe-123"

"""
Integration test for indexing a recipe in Elasticsearch via gRPC.
This test starts the gRPC server in a separate thread, sends a request to index a recipe,
and verifies that the recipe is indexed in Elasticsearch.

Required setup: elasticsearch must be running on localhost:9200
"""

class TestRecipeIndexIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Start the gRPC server in a separate thread
        cls.server = SearchServer(port=50051)
        cls.server_thread = threading.Thread(target=cls.server.start, daemon=True)
        cls.server_thread.start()

        # Give the server time to start
        time.sleep(2)

        # Set up Elasticsearch client
        cls.es_client = ElasticsearchClient().es_client

    @classmethod
    def tearDownClass(cls):
        # Cleanup: Remove test document from Elasticsearch
        if cls.es_client.exists(index=ES_INDEX, id=TEST_RECIPE_ID):
            cls.es_client.delete(index=ES_INDEX, id=TEST_RECIPE_ID)

        # Stop the gRPC server
        cls.server.stop()

    def test_index_recipe_success(self):
        # Connect to gRPC server
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = RecipeSearchServiceStub(channel)

            # Create test request
            request = IndexRecipeRequest(
                id=TEST_RECIPE_ID,
                title="Integration Test Recipe",
                instructions="Step 1: Run test. Step 2: Pass test.",
                notes="Integration test notes.",
                is_public=True
            )

            # Send request
            response = stub.IndexRecipe(request)
            self.assertTrue(response.success, f"gRPC response failed: {response.error_message}")

        # Verify document is indexed in Elasticsearch
        time.sleep(1)  # Small delay for indexing
        doc = self.es_client.get(index=ES_INDEX, id=TEST_RECIPE_ID)
        self.assertEqual(doc['_source']['title'], "Integration Test Recipe")
        self.assertEqual(doc['_source']['instructions'], "Step 1: Run test. Step 2: Pass test.")
        self.assertEqual(doc['_source']['notes'], "Integration test notes.")
        self.assertEqual(doc['_source']['isPublic'], True)

if __name__ == '__main__':
    unittest.main()
