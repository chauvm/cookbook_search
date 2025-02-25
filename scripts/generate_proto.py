import os
import subprocess

# Paths
PROTO_DIR = "./src/protos"
OUTPUT_DIR = "./src/generated"
OUTPUT_SEARCH_CLIENT_DIR = os.getenv("OUTPUT_SEARCH_CLIENT_DIR") or "/Users/rubybui/class/techcare/cookbook/cookbook_api/search_proxy/generated"

# Ensure output directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
if OUTPUT_SEARCH_CLIENT_DIR:
    os.makedirs(OUTPUT_SEARCH_CLIENT_DIR, exist_ok=True)

# Function to compile proto files
def compile_protos():
    for proto_file in os.listdir(PROTO_DIR):
        if proto_file.endswith(".proto"):
            input_path = os.path.join(PROTO_DIR, proto_file)
            print(f"Compiling {input_path}...")
            
            # Compile to both output directories
            for output in [OUTPUT_DIR, OUTPUT_SEARCH_CLIENT_DIR]:
                if output:
                    subprocess.run(
                        [
                            "python3", "-m", "grpc_tools.protoc",
                            f"-I{PROTO_DIR}",
                            f"--python_out={output}",
                            f"--grpc_python_out={output}",
                            input_path,
                        ],
                        check=True,
                    )

if __name__ == "__main__":
    compile_protos()
    print("Proto files compiled successfully.")
