import docker

# Create a Docker client
client = docker.from_env()

# Define container parameters
container_name = "redis-prod"
image_name = "redis:latest"

# Check if the container already exists
try:
    container = client.containers.get(container_name)
    if container.status == "running":
        print(f"Container '{container_name}' is already running.")
    else:
        container.start()
        print(f"Started container '{container_name}'.")
except Exception as e:
    print(e.__str__())

