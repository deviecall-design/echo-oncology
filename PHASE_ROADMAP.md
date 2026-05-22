# Echo Oncology — Complete Phase Roadmap (1-3)

## Phase 1: Surgical Intelligence MVP (6-8 weeks)
**Objective:** Prove brain cancer 3D surgical visualization + trajectory planning works

**Focus:**
- Cesium.js 3D brain visualization
- nnU-Net tumor segmentation (ONNX, in-browser)
- BraTS dataset integration
- Surgical planning UI
- Foundry OSDK sync

**Not in Phase 1:**
- Voice (Whisper)
- Analytics (Plausible)
- Collaboration (AppFlowy)
- Design tools (Penpot)
- Workflow builder (Flowise)
- Local LLM (Ollama)

---

## Phase 2: Clinical Reasoning + Ecosystem (8-10 weeks post-Phase 1)
**Objective:** Layer local inference, voice, collaboration, and analytics

### 2a: Local LLM Reasoning (Ollama)
- Interpret nnU-Net results → clinical notes
- Generate WHO/RANO staging reports
- Suggest surgical approaches
- Hospital edge deployment (zero data exfiltration)

### 2b: Voice Commands (Whisper)
- Intraop voice commands → 3D navigation
- Surgeon dictation → real-time clinical notes
- Voice alerts + feedback

### 2c: Hospital Collaboration (AppFlowy)
- Tumor board workspace
- Shared case reviews
- Clinical documentation
- Team coordination

### 2d: Privacy Analytics (Plausible)
- Adoption tracking (which surgeons use most)
- Workflow metrics (margin definition efficiency)
- Hospital telemetry (self-hosted)

### 2e: Design Collaboration (Penpot)
- UX/UI prototyping with radiologists + surgeons
- Design-to-code pipeline
- Shared design feedback

### 2f: Clinical Workflows (Flowise)
- No-code AI agent builder
- Surgeons/radiologists build custom decision workflows
- Visual workflow builder (visual → code)

---

## Phase 3: Scale + Defense Inversion (Post-Phase 2)
**Objective:** Apply patterns to Ember Echo (emergency response)

- Multimodal (voice + gesture + eye-tracking)
- Custom surgical AR (Ray-Ban Meta Skyler integration)
- Federated learning (hospital nodes sync to Foundry)
- Research partnerships (Victor Chang, Westmead)

---

## Repository Structure

```
echo-oncology/
├── README.md                    # Overview + quick start
├── PHASE_ROADMAP.md            # This file
├── dashboard/                   # Phase 1 MVP
│   ├── package.json
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── hooks/
│   │   └── data/
│   └── public/
├── ollama/                      # Phase 2a
│   ├── README.md
│   ├── Dockerfile
│   └── models/
├── whisper/                     # Phase 2b
│   ├── README.md
│   └── src/
├── appflowy/                    # Phase 2c
│   ├── README.md
│   └── docker-compose.yml
├── plausible/                   # Phase 2d
│   ├── README.md
│   └── docker-compose.yml
├── penpot/                      # Phase 2e
│   ├── README.md
│   └── docker-compose.yml
├── flowise/                     # Phase 2f
│   ├── README.md
│   └── docker-compose.yml
├── foundry-osdk/                # Backend
│   ├── README.md
│   └── src/
├── data/                        # BraTS + datasets
│   ├── brats/
│   └── sample-cases/
├── docs/                        # Technical docs
│   ├── architecture.md
│   ├── api.md
│   └── deployment.md
└── .env.example
```

---

## Tool Integration Points

| Tool | Phase | Integration | Data Flow |
|---|---|---|---|
| Cesium.js | 1 | 3D visualization | BraTS → 3D brain |
| nnU-Net | 1 | Segmentation | DICOM → tumor mesh |
| Foundry OSDK | 1-3 | Backend + ontology | Surgical plan → Foundry |
| **Ollama** | 2 | Local LLM | Segmentation results → clinical notes |
| **Whisper** | 2 | Voice input | Surgeon voice → commands + notes |
| **AppFlowy** | 2 | Collaboration | Case reviews → shared workspace |
| **Plausible** | 2 | Analytics | Usage metrics → hospital insights |
| **Penpot** | 2 | Design | Prototypes → React components |
| **Flowise** | 2 | Workflows | Visual builder → surgical logic |

---

## Installation (All Tools)

```bash
# Phase 1 MVP
cd dashboard && npm install

# Phase 2 Ecosystem (when ready)
docker compose -f ollama/docker-compose.yml up -d
docker compose -f appflowy/docker-compose.yml up -d
docker compose -f plausible/docker-compose.yml up -d
docker compose -f penpot/docker-compose.yml up -d
docker compose -f flowise/docker-compose.yml up -d

# Whisper (npm)
cd whisper && npm install openai whisper-1
```

---

## Success Criteria by Phase

### Phase 1
- ✅ 3D visualization renders BraTS cases
- ✅ nnU-Net segments tumors (>90% Dice)
- ✅ Margin definition UI works
- ✅ Foundry sync functional
- ✅ Helen Wheeler can demo it

### Phase 2
- ✅ Ollama generates clinical notes from segmentation
- ✅ Whisper voice commands → 3D navigation
- ✅ AppFlowy workspace syncs surgical plans
- ✅ Plausible tracks adoption metrics
- ✅ Penpot design → React components
- ✅ Flowise workflows integrated

### Phase 3
- ✅ Patterns scaled to Ember Echo
- ✅ Multi-hospital federation
- ✅ AR integration (Ray-Ban Meta)
- ✅ Research partnerships active

---

**Owner:** Deviecall | **Mission:** World's first healthcare AI with defense-grade spatial intelligence
