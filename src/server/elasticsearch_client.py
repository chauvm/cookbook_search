import logging
import os
from elasticsearch import Elasticsearch
from src.generated.recipe_index_pb2 import IndexRecipeRequest
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)


logger = logging.getLogger(__name__)

RECIPE_INDEX_NAME = "recipe"

class ElasticsearchClient:
    _instance = None

    def __new__(cls, host: str = 'localhost', port: int = 9200, username: str = 'elastic', password: str = None):
        if password is None:
            password = os.getenv('ES_PASSWORD')
        if not password:
            raise ValueError("ES_PASSWORD environment variable is not set.")

        if cls._instance is None:
            logger.info("Initializing Elasticsearch client...")
            cls._instance = super(ElasticsearchClient, cls).__new__(cls)
            cls._instance.es_client = Elasticsearch(
                hosts=[{
                    'host': host,
                    'port': port,
                    'scheme': 'https'  # Specify HTTPS scheme
                }],
                basic_auth=(username, password),
                verify_certs=False  # Disable SSL verification for self-signed certificates
            )
            logger.info("Elasticsearch client initialized.")
        return cls._instance


    def search_recipe(self, phrase: str, index: str = "recipes", field: str = "title", size: int = 10):
        """
        Search for a phrase in the indexed recipe.
        
        :param phrase: The phrase to search for.
        :param index: The Elasticsearch index name where recipes are stored.
        :param field: The field within the index to search in.
        :param size: The number of results to return.
        :return: List of matching recipes.
        """
        query = {
            "query": {
                "match_phrase": {
                    field: phrase
                }
            },
            "size": size
        }
        
        response = self.es_client.search(index=index, body=query)
        
        results = [hit["_source"] for hit in response.get("hits", {}).get("hits", [])]
        return results
    
    def index_recipe(self, recipe: IndexRecipeRequest): 
        """
        Index a recipe in Elasticsearch.
        
        :param recipe: The recipe content to index.
        :param index: The Elasticsearch index name where recipes are stored.
        """
        index = RECIPE_INDEX_NAME
        recipe_id = recipe.id
        document = {
            "title": recipe.title,
            "instructions": recipe.instructions,
            "notes": recipe.notes,
            "isPublic": recipe.is_public
        }
        response = self.es_client.index(
            index=index, 
            id = recipe_id, 
            document=document
        )
        return response