import logging
import os
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

# from recipe_search_service_pb2 import SearchRequest  # Make sure you have this import if using the enum

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)
logger.info("Logger is working!")  # Debug log to check logger initialization


class ElasticsearchClient:
    _instance = None

    def __new__(
        cls,
        host: str = "localhost",
        port: int = 9200,
        username: str = "elastic",
        password: str = None,
    ):
        if password is None:
            password = os.getenv("ES_PASSWORD")
        if not password:
            raise ValueError("ES_PASSWORD environment variable is not set.")

        if cls._instance is None:
            logger.info("Initializing Elasticsearch client...")
            cls._instance = super().__new__(cls)
            cls._instance.es_client = Elasticsearch(
                hosts=[
                    {
                        "host": host,
                        "port": port,
                        "scheme": "https",  # Use HTTPS
                    }
                ],
                basic_auth=(username, password),
                verify_certs=False,  # For self-signed certs
            )
            logger.info("Elasticsearch client initialized.")
        return cls._instance

    @staticmethod
    def _build_generic(key: str, field: str, value: str) -> dict:
        """
        For queries that share the structure: { key: { field: value } }
        E.g. {"match": {field: value}}, {"term": {field: value}}, etc.
        """
        return {key: {field: value}}

    @staticmethod
    def build_es_query(
        query_type_enum: int,
        field: str,
        value: str,
        fields: list = None,
        range_filter: dict = None,
    ):
        """
        Go directly from the QueryType enum to an Elasticsearch query dict.
        - MATCH, MATCH_PHRASE, TERM => same structure (use _build_generic).
        - MULTI_MATCH, EXISTS, RANGE => special shapes.
        """
        # If you have a real SearchRequest.QueryType, do:
        #
        #   enum_name = SearchRequest.QueryType.Name(query_type_enum)
        #
        # For demonstration, let's define a quick local map:
        enum_map = {
            0: "match",
            1: "multi_match",
            2: "match_phrase",
            3: "term",
            4: "exists",
            5: "range",
        }
        enum_name = enum_map.get(query_type_enum)
        if not enum_name:
            raise ValueError(f"Invalid query_type enum: {query_type_enum}")

        query_key = enum_name.lower()

        # Special cases or fallback to generic
        if query_key == "multi_match":
            if not fields:
                raise ValueError("Fields must be specified for multi_match query.")
            return {
                "multi_match": {
                    "query": value,
                    "fields": fields,
                }
            }
        elif query_key == "exists":
            return {
                "exists": {
                    "field": field
                }
            }
        elif query_key == "range":
            if not range_filter:
                raise ValueError("Range filter cannot be empty for range query.")
            return {
                "range": {
                    field: range_filter
                }
            }
        else:
            # For match, match_phrase, term, etc.
            return ElasticsearchClient._build_generic(query_key, field, value)

    def search_recipe(
        self,
        query_type: int,
        field: str,
        value: str,
        fields: list = None,
        range_filter: dict = None,
        sort: list = None,
        index: str = "recipes",
        size: int = 10,
    ):
        """
        Search for a phrase in the indexed recipe, going directly from enum -> query.
        """
        # Because build_es_query is a staticmethod, we call it via the class
        query_part = ElasticsearchClient.build_es_query(
            query_type, field, value, fields, range_filter
        )

        query = {"query": query_part, "size": size}
        if sort:
            query["sort"] = [{s["field"]: {"order": s["order"]}} for s in sort]

        logger.warning(f"Executing ES query: {query}")

        response = self.es_client.search(index=index, body=query)
        return response
