# Echo Oncology Sprint 1 — Execution Checklist

**Project:** Echo Oncology (Surgical Intelligence for Brain Cancer)  
**Sprint:** 1 — E2E Pipeline Validation  
**Duration:** Weeks 1–2 (May 29 – June 12, 2026)  
**Status:** 🟢 STARTING NOW  

---

## 📋 Pre-Execution Checklist

### ✅ Deliverables Ready

- [x] Mission Control Dashboard (HTML) — task tracking + tech stack visualization
- [x] Python Pipeline Module (echo_pipeline.py) — production-ready code structure
- [x] Test Suite (tests_echo_pipeline.py) — comprehensive test coverage
- [x] Technical Documentation (SPRINT1_TECHNICAL_DOCUMENTATION.md) — architecture + specs
- [x] This Execution Checklist

### ⏳ Environment Setup (You)

- [ ] Clone/access Echo Oncology GitHub repo
- [ ] Create Python 3.9+ virtual environment
- [ ] Install dependencies: PyTorch, transformers, nibabel, scikit-image, trimesh, pytest
- [ ] Download BraTS 2021 dataset (~6.5GB) from https://www.synapse.org/#!Synapse:syn25829067
- [ ] Verify BraTS structure: `./data/brats/BraTS21_00000/BraTS21_00000_t1.nii.gz`, etc.

### 🤝 Communication Setup

- [ ] Weekly sync scheduled: Mondays 9 AM Sydney time
- [ ] Slack/email updates: Flag blockers ASAP (don't wait until Friday)
- [ ] GitHub branch name: `feat/sprint1-e2e-pipeline` (or your convention)
- [ ] Progress tracking: Use Mission Control dashboard weekly

---

## 📅 Week 1: Pipeline Infrastructure (May 29 – June 4)

### Day 1–2: DICOM Loader + nnU-Net Integration

#### Task 1️⃣ — DICOM Loader Test (1–2 hours)
**Owner:** Me  
**Effort:** 1–2 hrs  
**Blocker Level:** 🔴 CRITICAL (unblocks Task 2)

**What you do:**
- [ ] Confirm BraTS dataset downloaded (check `./data/brats/BraTS21_00000/` exists)
- [ ] Run sample DICOM loader test:
  ```bash
  python -c "from echo_pipeline import DicomLoader; \
  loader = DicomLoader(); \
  img, meta = loader.load('./data/brats/BraTS21_00000/BraTS21_00000_t1.nii.gz'); \
  print(f'Loaded: {meta[\"shape\"]}')"
  ```
- [ ] Report any file-not-found or corruption errors

**Success:** Console prints shape like `(240, 240, 155)` with no errors

---

#### Task 2️⃣ — nnU-Net Inference Integration (2–3 hours)
**Owner:** Me  
**Effort:** 2–3 hrs  
**Blocker Level:** 🔴 CRITICAL (unblocks Task 3)

**What you do:**
- [ ] Let pipeline download model (first run will download from HuggingFace, ~300MB)
- [ ] Monitor for CUDA/memory issues (we run on CPU, should be fine)
- [ ] Test inference on 1 sample case:
  ```bash
  python -c "from echo_pipeline import SegmentationPipeline, DicomLoader; \
  loader = DicomLoader(); \
  img, _ = loader.load('./data/brats/BraTS21_00000/BraTS21_00000_t1.nii.gz'); \
  seg = SegmentationPipeline().segment(img); \
  print(f'Segmented: {seg.shape}, classes: {list(set(seg.flatten()))}')"
  ```
- [ ] Report inference time and memory usage

**Success:** Console prints segmentation shape matching input + class list like `[0, 1, 2, 4]`

---

### Day 3: Mesh Generation + Three.js

#### Task 3️⃣ — Mesh Generation & Export (1–2 hours)
**Owner:** Me  
**Effort:** 1–2 hrs  
**Blocker Level:** 🟠 HIGH (unblocks Task 4)

**What you do:**
- [ ] Run mesh generation test:
  ```bash
  python -c "from echo_pipeline import MeshGenerator; \
  import numpy as np; \
  mask = np.zeros((50, 50, 50), dtype=np.uint8); \
  mask[10:40, 10:40, 10:40] = 1; \
  gen = MeshGenerator(); \
  v, f = gen.generate(mask); \
  print(f'Mesh: {len(v)} vertices, {len(f)} faces')"
  ```
- [ ] Export test mesh:
  ```bash
  python -c "from echo_pipeline import MeshGenerator; \
  import numpy as np; \
  mask = np.zeros((50, 50, 50), dtype=np.uint8); \
  mask[10:40, 10:40, 10:40] = 1; \
  gen = MeshGenerator(); \
  v, f = gen.generate(mask); \
  gen.export_gltf(v, f, './test_mesh.glb')"
  ```
- [ ] Confirm `./test_mesh.glb` created and >1KB

**Success:** File created, no errors in console

---

#### Task 4️⃣ — Three.js Integration (1–2 hours)
**Owner:** Me  
**Effort:** 1–2 hrs  
**Blocker Level:** 🟠 HIGH (unblocks Task 5)

**What you do:**
- [ ] Open your React codebase (assuming Next.js 14 + three.js)
- [ ] I'll provide a `BrainViewer.tsx` component that loads the `.glb` file
- [ ] Test in browser:
  - [ ] Upload `./test_mesh.glb` to public folder
  - [ ] Load component, confirm mesh visible
  - [ ] Test rotation/zoom controls
  - [ ] Check console for WebGL errors (should be none)
- [ ] Report any rendering issues

**Success:** Mesh visible in 3D viewer, controls work, 60fps

---

### Day 4–5: Demo & Validation

#### Task 5️⃣ — End-to-End Demo (2–3 hours)
**Owner:** Me  
**Effort:** 2–3 hrs  
**Blocker Level:** 🟡 MEDIUM (deliverable)

**What you do:**
- [ ] Run full pipeline on 5 BraTS cases:
  ```bash
  python run_demo.py --cases 5 --output_dir ./demo_output
  ```
  *(I'll provide `run_demo.py` script)*
- [ ] Confirm all 5 cases complete without errors
- [ ] Check `./demo_output/` for 5 `.glb` files
- [ ] Load each in browser viewer, confirm rendering
- [ ] Report processing time and any issues

**Success:** 5 meshes generated, all render correctly, time logged

---

## 📅 Week 2: Validation & Testing (June 5–12)

### Day 1–2: Full Validation

#### Task 6️⃣ — 100-Case BraTS Validation (4–6 hours)
**Owner:** Me  
**Effort:** 4–6 hrs  
**Blocker Level:** 🟡 MEDIUM (research deliverable)

**What you do:**
- [ ] Kick off validation script (runs unattended):
  ```bash
  python validate_brats.py --cases 100 --output_dir ./validation_results
  ```
- [ ] Monitor progress (~1 hr per 10 cases on CPU, so ~10 hours total, recommend overnight)
- [ ] Check for crashes/errors in logs
- [ ] Once complete, confirm results file: `./validation_results/metrics.csv`

**Success:** Metrics file exists with Dice scores for 100 cases, mean ≥0.92

---

### Day 3: Error Analysis

#### Task 7️⃣ — Error Analysis & Documentation (2–3 hours)
**Owner:** Me (with your input)  
**Effort:** 2–3 hrs  
**Blocker Level:** 🟡 MEDIUM (research deliverable)

**What you do:**
- [ ] Review metrics report: `./validation_results/metrics.csv`
- [ ] I'll analyze failure cases (Dice <0.70)
- [ ] You review error analysis document: `SPRINT1_ERROR_ANALYSIS.md`
- [ ] Provide clinical feedback: do failure cases look reasonable (e.g., small tumors, artifacts)?
- [ ] Approve or flag for investigation

**Success:** Error analysis doc complete, <5% failure rate acceptable

---

### Day 4: Documentation

#### Task 8️⃣ — Documentation & Demo Ready (3–4 hours)
**Owner:** Me  
**Effort:** 3–4 hrs  
**Blocker Level:** 🟢 LOW (polish)

**What you do:**
- [ ] Review final documentation:
  - [ ] README.md (setup instructions)
  - [ ] ARCHITECTURE.md (diagrams, data flow)
  - [ ] METRICS.md (Dice scores, timing, specs)
- [ ] Watch demo video (5 meshes, different angles)
- [ ] Approve or request changes
- [ ] Merge feature branch to main

**Success:** All docs reviewed, demo video created, PR merged

---

## 🎯 Success Criteria Checklist

### Must-Have (Definition of Done)

- [ ] **DICOM Loader:** Successfully loads 100 BraTS cases without corruption
- [ ] **Segmentation:** nnU-Net inference outputs valid masks for all 100 cases
- [ ] **Mesh Generation:** Marching cubes produces valid meshes (no degenerate faces)
- [ ] **Three.js Rendering:** All meshes render correctly in browser (60fps)
- [ ] **Dice Score:** Mean ≥0.92 on 100 BraTS cases
- [ ] **Failure Rate:** <5% cases with Dice <0.70
- [ ] **Processing Time:** <8 hours for 100 cases on CPU
- [ ] **Demo Readiness:** 5 cases fully processed, visualized, video created
- [ ] **Tests Pass:** `pytest tests_echo_pipeline.py` passes with ≥90% coverage
- [ ] **Documentation:** README, Architecture, Metrics docs complete

### Nice-to-Have (Bonus)

- [ ] Quantization for faster inference
- [ ] GPU support (if CUDA available)
- [ ] Web UI for uploading custom DICOM files
- [ ] Dice score comparison plot (ours vs baseline)

---

## 🚨 Blockers & Escalation

### If you encounter blockers:

1. **DICOM file not found:** Check BraTS directory structure, re-download if needed
2. **Memory overflow:** Reduce batch size, or process one case at a time
3. **CUDA not available:** Confirm `device='cpu'` in pipeline initialization
4. **Model download fails:** Check internet connection, try manual download from HuggingFace
5. **Three.js not loading mesh:** Check CORS settings, glTF file size, console errors

**Escalation:**
- Day 1–2 blockers: Fix immediately (unblocks rest of sprint)
- Day 3+ blockers: Flag on Monday sync, discuss mitigation

---

## 📊 Weekly Status Template

**Week 1 Summary (due Friday 5 PM Sydney):**
```
✅ Completed:
- Task 1: DICOM loader (1.5 hrs)
- Task 2: nnU-Net integration (2.5 hrs)
- Task 3: Mesh generation (1.5 hrs)
- Task 4: Three.js integration (1.5 hrs)

⏳ In Progress:
- Task 5: Demo on 5 cases (50% complete)

🚧 Blockers:
- None

📈 Metrics:
- Test sample processed in 8 minutes
- Mesh quality: all faces valid
- Three.js FPS: 60 stable
```

**Week 2 Summary (due Friday 5 PM Sydney):**
```
✅ Completed:
- Task 5: Demo on 5 cases
- Task 6: 100-case validation
- Task 7: Error analysis
- Task 8: Documentation

📊 Final Metrics:
- Mean Dice: 0.927
- Failure rate: 2.3% (2/100 cases)
- Processing time: 7.2 hrs (100 cases on CPU)
- Memory peak: 2.8GB
- Demo ready: YES

🎯 Sprint 1 Status: ✅ COMPLETE
```

---

## 📞 Communication Channels

- **Weekly Sync:** Mondays 9 AM Sydney time (Slack/Zoom)
- **Blockers:** Slack message ASAP (don't wait for sync)
- **Code Review:** GitHub PR review before merge
- **Documentation:** Google Docs or GitHub comments
- **Demo Delivery:** GitHub release + video link

---

## 🎓 Reference Links

- **nnU-Net Paper:** https://arxiv.org/abs/1904.08128
- **BraTS Challenge:** https://www.med.upenn.edu/cbica/brats/
- **Three.js GLTFLoader:** https://threejs.org/docs/#examples/en/loaders/GLTFLoader
- **PyTorch Inference:** https://pytorch.org/docs/stable/inference.html

---

## Next Steps (Right Now)

1. **You:** Set up environment + download BraTS
2. **Me:** Start Task 1 (DICOM loader testing)
3. **Together:** Monday 9 AM sync to review Week 1 progress

**Let's ship Phase 1. 🚀**

---

**Last Updated:** May 29, 2026  
**Sprint Status:** 🟢 STARTING  
**Estimated Completion:** June 12, 2026
