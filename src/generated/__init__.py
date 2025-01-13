import os
import sys

# Add the current directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from . import pingpong_pb2
from . import pingpong_pb2_grpc
