import logging
import os
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

load_dotenv()

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)
logger.info("Logger is working!")  # Debug log to check logger initialization

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

    def search_recipe(self, query_type: str, field: str, value: str, fields: list = None, range_filter: dict = None, sort: list = None, index: str = "recipes", size: int = 10):
        """
        Search for a phrase in the indexed recipe.
        """
        query = {}

        # Validate query_type and value
        if query_type not in ["match", "multi_match", "match_phrase", "term", "exists", "range"]:
            raise ValueError(f"Invalid query_type: {query_type}")

        if query_type not in ["exists", "range"] and not value:
            raise ValueError("Search value cannot be empty for this query type.")

        if query_type == "match":
            query["query"] = {"match": {field: value}}
        elif query_type == "multi_match":
            if not fields:
                raise ValueError("Fields must be specified for multi_match query.")
            query["query"] = {"multi_match": {"query": value, "fields": fields}}
        elif query_type == "match_phrase":
            query["query"] = {"match_phrase": {field: value}}
        elif query_type == "term":
            query["query"] = {"term": {field: value}}
        elif query_type == "exists":
            query["query"] = {"exists": {"field": field}}
        elif query_type == "range":
            if not range_filter:
                raise ValueError("Range filter cannot be empty for range query.")
            query["query"] = {"range": {field: range_filter}}

        if sort:
            query["sort"] = [{s["field"]: {"order": s["order"]}} for s in sort]

        query["size"] = size

        logger.warning(f"Executing ES query: {query}")  # Fixed: use logger.warning, not logger.warnings

        # Execute query
        response = self.es_client.search(index=index, body=query)

        return response
