from src.server.elasticsearch_client import ElasticsearchClient

def test_connection():
    es_client = ElasticsearchClient()
    try:
        # Check if Elasticsearch is up
        if es_client.es_client.ping():
            print("Connected to Elasticsearch successfully!")
        else:
            print("Failed to connect to Elasticsearch.")
    except Exception as e:
        print(f"Error: {e}")

def test_search():
    es_client = ElasticsearchClient()
    while True:
        phrase = input("Enter search phrase (or type 'exit' to quit): ")
        if phrase.lower() == 'exit':
            break
        results = es_client.search_recipe(phrase)
        print("Search Results:", results)

def test_recipe_indexing():
    es_client = ElasticsearchClient()
    recipe = {
        "id": '123',
        "title": "Example Recipe",
        "instructions": "Mix ingredients and bake at 350 degrees.",
        "notes": "Use organic ingredients for better taste.",
        "isPublic": True
    }
    res = es_client.index_recipe(recipe)
    print("Recipe indexed successfully:", res)

if __name__ == "__main__":
    test_connection()
    test_search()
    test_recipe_indexing()