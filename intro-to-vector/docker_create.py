import docker

# Create a Docker client
client = docker.from_env()

# Define container parameters
container_name = "my_container"
image_name = "redis:latest"
command = "/bin/bash"  # Replace with your desired command
ports = {'6379/tcp': 6379}  # Port mapping (host_port:container_port)

# Create the container
container = client.containers.create(
    image=image_name,
    name=container_name,
    command=command,
    ports=ports,
    detach=True  # Run the container in the background
)

# Start the container
container.start()

# Print container details
print(f"Created and started container '{container_name}' (ID: {container.id})")
