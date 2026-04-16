# Running Ollama via Docker on Ubuntu

## Prerequisites

- Ubuntu 20.04 or later
- Docker installed ([Install Docker](https://docs.docker.com/engine/install/ubuntu/))
- (Optional) NVIDIA GPU + [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html) for GPU acceleration

---

## Step 1: Pull the Ollama Docker Image

```bash
docker pull ollama/ollama
```

---

## Step 2: Run the Container

### CPU Only

```bash
docker run -d \
  --name ollama \
  -p 11434:11434 \
  -v ollama:/root/.ollama \
  ollama/ollama
```

### With NVIDIA GPU Support

```bash
docker run -d \
  --name ollama \
  --gpus all \
  -p 11434:11434 \
  -v ollama:/root/.ollama \
  ollama/ollama
```

### Flags Explained

| Flag | Description |
|---|---|
| `-d` | Run container in background (detached) |
| `--name ollama` | Name the container "ollama" |
| `-p 11434:11434` | Map host port 11434 to container port 11434 |
| `-v ollama:/root/.ollama` | Persist downloaded models to a Docker volume |
| `--gpus all` | Enable all available NVIDIA GPUs |

---

## Step 3: Pull a Model

```bash
docker exec -it ollama ollama pull llama3.2
```

### Other Popular Models

```bash
docker exec -it ollama ollama pull mistral       # Great for coding
docker exec -it ollama ollama pull gemma3        # Google's model
docker exec -it ollama ollama pull phi4-mini     # Lightweight & fast
docker exec -it ollama ollama pull llama3.1      # Larger, more capable
```

### Model RAM Requirements

| Model | Min RAM | Best For |
|---|---|---|
| `phi4-mini` | 4 GB | Speed, lightweight tasks |
| `llama3.2` (3B) | 4 GB | General purpose |
| `mistral` (7B) | 8 GB | Coding, reasoning |
| `llama3.1` (8B) | 8 GB | Best open-source model |
| `gemma3` (12B) | 16 GB | Google's flagship |

---

## Step 4: Chat with the Model

### Option A — Interactive CLI

```bash
docker exec -it ollama ollama run llama3.2
```

Type your message and press `Enter`. Press `Ctrl+D` to exit.

### Option B — REST API

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "llama3.2",
  "messages": [
    { "role": "user", "content": "Hello! What can you do?" }
  ]
}'
```

### Option C — Python

```python
import requests

response = requests.post("http://localhost:11434/api/chat", json={
    "model": "llama3.2",
    "messages": [{"role": "user", "content": "Hello!"}],
    "stream": False
})

print(response.json()["message"]["content"])
```

---

## Step 5: (Optional) Add a Web UI

Run **Open WebUI** for a browser-based ChatGPT-like interface:

```bash
docker run -d \
  --name open-webui \
  --network host \
  -v open-webui:/app/backend/data \
  -e OLLAMA_BASE_URL=http://127.0.0.1:11434 \
  ghcr.io/open-webui/open-webui:main
```

Then open **http://localhost:8080** in your browser.

---

## Useful Commands

```bash
# List all downloaded models
docker exec -it ollama ollama list

# Remove a model
docker exec -it ollama ollama rm mistral

# Check running containers
docker ps

# Stop the container
docker stop ollama

# Start the container again
docker start ollama

# View container logs
docker logs ollama

# Remove the container entirely
docker rm ollama

# Remove the docker image
docker rmi ollama/ollama
```

---

## Troubleshooting

### Port 11434 Already in Use

Check what is using the port:

```bash
sudo lsof -i :11434
```

If Ollama is already installed natively (e.g., via Snap), either use it directly or stop it first:

```bash
sudo kill <PID>      # Kill the native process
```

Or use a different port for Docker:

```bash
docker run -d --name ollama -p 11435:11434 -v ollama:/root/.ollama ollama/ollama
```

### Container Not Starting

```bash
# Check logs for errors
docker logs ollama

# Remove and recreate the container
docker rm ollama
docker run -d --name ollama -p 11434:11434 -v ollama:/root/.ollama ollama/ollama
```

### Free Up Disk Space

```bash
# Remove unused/dangling images
docker image prune -f

# Remove specific image
docker rmi ollama/ollama
```

---

## Quick Reference Card

```bash
# 1. Pull image
docker pull ollama/ollama

# 2. Run container
docker run -d --name ollama -p 11434:11434 -v ollama:/root/.ollama ollama/ollama

# 3. Pull a model
docker exec -it ollama ollama pull llama3.2

# 4. Chat!
docker exec -it ollama ollama run llama3.2
```

---


> 🔗 Browse all available models at [ollama.com/library](https://ollama.com/library)
