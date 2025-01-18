import os
from dotenv import load_dotenv
from src.server.ping_pong_server import PingPongServer

import sys
# print('\n'.join(sys.path))


def main():
    load_dotenv()  # This loads the variables from .env
    port = int(os.getenv('GRPC_PORT', 50051))  # Default to 50051 if not set
    server = PingPongServer(port)
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()

if __name__ == "__main__":
    main()