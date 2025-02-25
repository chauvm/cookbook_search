import os
import subprocess

"""
usage: python3 generate_proto.py
"""

# Paths
PROTO_DIR = "./src/protos"
OUTPUT_DIR = "./src/generated"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Function to compile proto files
def compile_protos():
    for proto_file in os.listdir(PROTO_DIR):
        if proto_file.endswith(".proto"):
            input_path = os.path.join(PROTO_DIR, proto_file)
            print(f"Compiling {input_path}...")
            subprocess.run(
                [
                    "python3", "-m", "grpc_tools.protoc",
                    f"-I{PROTO_DIR}",
                    f"--python_out={OUTPUT_DIR}",
                    f"--grpc_python_out={OUTPUT_DIR}",
                    input_path,
                ],
                check=True,
            )

if __name__ == "__main__":
    compile_protos()
    print("Proto files compiled successfully.")
