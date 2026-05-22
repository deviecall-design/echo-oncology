# Ollama — Echo Oncology Local Inference

Local LLM inference layer for Edge deployment in hospital networks.

## Models

- `llama3.2` — Primary clinical reasoning
- `gemma3` — Fast inference for real-time surgical alerts
- Custom fine-tuned (Phase 3) — Echo Oncology clinical reasoning

## Use Cases

1. Interpret nnU-Net segmentation results → plain-English clinical findings
2. Generate WHO/RANO staging reports from imaging data
3. Suggest surgical approach based on tumor location + eloquent cortex proximity
4. Post-op monitoring report generation

## Setup

```bash
# Install
curl -fsSL https://ollama.com/install.sh | sh

# Pull models
ollama pull llama3.2
ollama pull gemma3

# Run API
ollama serve  # starts on localhost:11434

# Test
curl http://localhost:11434/api/chat -d '{
  "model": "llama3.2",
  "messages": [{
    "role": "user",
    "content": "Interpret: nnU-Net confidence 94.2%, tumor volume 3.2cm3, Grade IV glioblastoma. Generate surgical planning note."
  }],
  "stream": false
}'
```

## Hospital Edge Deployment

```bash
# Docker deployment (no external network required)
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

# Air-gapped deployment (hospital network isolation)
docker pull ollama/ollama  # one-time, before isolation
docker run --network none ollama/ollama  # zero external access
```
