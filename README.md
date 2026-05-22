# Echo Oncology — Brain Cancer Surgical Intelligence Platform

**World's first clinical AI applying defense-grade spatial intelligence to brain cancer surgery.**

Architecture: Palantir AIP + Anduril Lattice OS pattern (inverted to healthcare) + Cesium.js 3D surgical visualization + Ollama local inference.

## Tech Stack

| Layer | Technology |
|---|---|
| 3D Visualization | Cesium.js (Anduril EagleEye pattern) |
| Frontend | Next.js 14 + React 18 + TypeScript |
| DICOM Processing | cornerstone3D + dcmjs |
| Tumor Segmentation | nnU-Net v2 (ONNX Runtime, in-browser) |
| Local LLM Inference | Ollama (clinical reasoning, edge deployment) |
| Backend | Palantir Foundry OSDK |
| Deployment | Vercel |
| Dataset | BraTS 2023 (Phase 1), Australian clinical data (Phase 2) |

## Clinical Scope

Brain cancer (gliomas, WHO 2021 molecular classification) — five-phase continuum:

1. **Detection** — Ghost Murmur early signal integration
2. **Identify** — 3D margin definition + severity staging (WHO/RANO)
3. **Management** — Surgeon trajectory simulation + proximity quantification
4. **Applied Treatment** — Intraoperative navigation + brain shift compensation
5. **Roadmap** — Post-op recurrence monitoring

## Ollama Integration (Phase 2 - Local Clinical Reasoning)

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Run clinical reasoning model
ollama run llama3.2

# Or launch with OpenClaw integration
ollama launch openclaw
```

Ollama enables **edge deployment** in hospital networks:
- Zero patient data leaves the hospital
- Local LLM interprets imaging findings
- Generates clinical notes from segmentation results
- Integrates with Foundry ontology via OSDK

## Build Phases

- **Phase 1 (6-8 weeks):** Echo Oncology Surgical POC — 3D visualization + surgical planning
- **Phase 2 (8-10 weeks):** Ghost Murmur early detection layer + Ollama clinical reasoning
- **Phase 3:** Transfer architectural patterns to Ember Echo (emergency response)

## Deployment

Live: https://echo-deploy-mauve.vercel.app

## Owner

Deviecall — Damien Callaghan | deviecall-design/echo-oncology

---

*Built on the architectural pattern of Anduril EagleEye + Palantir AIP — inverted from defense to clinical oncology.*
