import os
import sys

# Add the current directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from . import search_pb2
from . import search_pb2_grpc
