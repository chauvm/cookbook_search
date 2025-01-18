from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import os

class ESClient():
    def __init__(self):
        ELASTICSEARCH_PORT = int(os.getenv('ELASTICSEARCH_PORT', 9200))
        ELASTICSEARCH_HOST = os.getenv('ELASTICSEARCH_HOST', 'localhost')
        ELASTICSEARCH_USER = os.getenv('ELASTICSEARCH_USER', 'elastic')
        ELASTICSEARCH_PWD = os.getenv('ELASTICSEARCH_PWD', '0jl39Zi9Uj8fpgg9W6H8J58k')
        print(ELASTICSEARCH_PORT, ' ', ELASTICSEARCH_HOST, ' ', ELASTICSEARCH_USER, ' ', ELASTICSEARCH_PWD)

        self.es_client = Elasticsearch(
            [{'host': ELASTICSEARCH_HOST, 'port': ELASTICSEARCH_PORT, 'scheme': 'https'}], 
            basic_auth=(ELASTICSEARCH_USER, ELASTICSEARCH_PWD),
            verify_certs=False
            )

    def es_ping(self):
        if self.es_client.ping():
            print("Successfully connected to Elasticsearch!")
        else: 
            print("Could not connect to Elasticsearch.")

    def create_index(self, index_name: str):
        if not self.es_client.indices.exists(index=index_name):
            self.es_client.indices.create(index=index_name)
            print(f"Index {index_name} created.")
        else:
            print(f"Index {index_name} already exists.")

    def insert_document(self, doc_id, document):
        self.es_client.index(
            index=self.index_name,
            id=doc_id,
            body=document
        )
        print(f"Document inserted into {self.index_name}.")

    def bulk_insert(self, index_name, documents):
        """
        Perform a bulk insert into the specified index.
        """
        actions = [
            {
                "_op_type": "index",  # Operation type (index)
                "_index": index_name,  # Target index
                "_id": doc.get("id"),  # Document ID (optional, can auto-generate if omitted)
                "_source": doc  # The document data
            }
            for doc in documents
        ]

        success, _ = bulk(self.es_client, actions)
        print(f"Successfully inserted {success} documents into index {index_name}.")


es_client = ESClient()
es_client.es_ping()
es_client.create_index("recipes")
recipes = [
        {"id": "101", "title": "Spaghetti Bolognese", "ingredients": ["spaghetti", "tomato sauce", "beef"], "instructions": "Cook pasta and mix with sauce."},
        {"id": "102", "title": "Chicken Curry", "ingredients": ["chicken", "curry powder", "coconut milk"], "instructions": "Cook chicken and add curry."}
    ]

es_client.bulk_insert("recipes", recipes)

response = es_client.es_client.get(index='recipes', id="101")

# # Print the document
print(response['_source'])