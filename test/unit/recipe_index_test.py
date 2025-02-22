import unittest
from unittest.mock import patch, MagicMock
from src.generated.recipe_index_pb2 import IndexRecipeRequest, IndexRecipeResponse
from src.server.server import RecipeIndexService

class TestRecipeIndexService(unittest.TestCase):
    def setUp(self):
        patcher = patch('src.server.server.ElasticsearchClient')
        self.mock_es_client = patcher.start()
        self.addCleanup(patcher.stop)
        self.service = RecipeIndexService()

        self.mock_request = IndexRecipeRequest(
            id="1",
            title="Example Recipe",
            instructions="Mix ingredients and bake at 350 degrees.",
            notes="Use organic ingredients for better taste.",
            is_public=True
        )

    def test_index_recipe_success(self):
        # Mock the Elasticsearch client's index_recipe method
        self.mock_es_client.return_value.index_recipe.return_value = {"status": "201"}
        context = MagicMock()  # Mock the gRPC context

        # Call the service method
        response = self.service.IndexRecipe(self.mock_request, context)

        # Assertions
        self.mock_es_client.return_value.index_recipe.assert_called_once_with(recipe={
            "id": "1",
            "title": "Example Recipe",
            "instructions": "Mix ingredients and bake at 350 degrees.",
            "notes": "Use organic ingredients for better taste.",
            "isPublic": True
        })
        self.assertIsInstance(response, IndexRecipeResponse)
        self.assertTrue(response.success)
        self.assertEqual(response.error_message, "")

    def test_index_recipe_failure(self):
        # Mock the Elasticsearch client's index_recipe method to raise an exception
        self.mock_es_client.return_value.index_recipe.side_effect = Exception("Elasticsearch error")
        context = MagicMock()
        # call the service
        response = self.service.IndexRecipe(self.mock_request, context)
        # assertions
        self.assertIsInstance(response, IndexRecipeResponse)
        self.assertFalse(response.success)
        self.assertEqual(response.error_message, "Elasticsearch error")    

if __name__ == '__main__':
    unittest.main()