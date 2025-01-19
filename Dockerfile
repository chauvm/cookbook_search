ARG INSTALL_PYTHON_VERSION=3.11.3

FROM python:${INSTALL_PYTHON_VERSION}-slim-bullseye AS builder

WORKDIR /app

# Copy requirements first for better cache utilization
COPY requirements requirements
RUN pip install --no-cache -r requirements/prod.txt

# Copy the rest of the application
# Copy the rest of the application code into the container
COPY src /app/src
COPY test /app/test
COPY .env.example /app/.env

# Use environment variables from .env file
ENV $(cat .env | xargs)

# Expose the port specified in .env
EXPOSE ${GRPC_PORT}

# Run the application
CMD ["python3", "-u" ,"-m", "src.main"]