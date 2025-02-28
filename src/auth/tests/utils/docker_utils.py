import os
import docker
import time

import docker.errors

def is_container_ready(container: docker.DockerClient)-> bool:
    container.reload()
    return container.status=="running"

def wait_for_stable_status(container: docker.DockerClient, stable_duration:int=3, interval:int=1)-> bool:
    start_time = time.time()
    stable_count = 0

    while time.time()-start_time < stable_duration:
        if is_container_ready(container=container):
            stable_count+=1
        if stable_count>= stable_duration/interval:
            return True
        time.sleep(interval)
    return False

def start_database_container()-> docker.DockerClient:
    scripts_dir = os.path.abspath("./scripts")
    client = docker.from_env()
    container_name = "test-db"

    try:
        existing_container = client.containers.get(container_name)
        existing_container.stop()
        existing_container.remove(force=True)
    except docker.errors.NotFound:
        pass
    container_config = {
        "name": container_name,
        "image": "postgres:16.1-alpine3.19",
        "detach": True,
        "ports": {"5432": "5434"},
        "environment": {
            "POSTGRES_PASSWORD": "postgres",
            "POSTGRES_USER": "postgres",
        },
        "volumes": [
            f"{scripts_dir}:/docker-entrypoint-initdb.d",
        ],
        # "network_mode": "dev_network",
    }
    container = client.containers.run(**container_config)
    while not is_container_ready(container=container):
        time.sleep(4)
    if not wait_for_stable_status(container=container):
        raise RuntimeError(f"Container {container_name} did not stablize in the specified time.")
    return container