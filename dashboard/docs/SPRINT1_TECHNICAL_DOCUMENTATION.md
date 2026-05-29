# Echo Oncology Sprint 1 Technical Documentation

**Title:** E2E Pipeline Validation (Weeks 1–2)  
**Date:** May 29, 2026  
**Author:** Claude Code  
**Status:** In Development

---

## 1. Executive Summary

Sprint 1 validates the complete Echo Oncology radiomics pipeline:
- **Input:** Brain MRI (DICOM/NIfTI)
- **Processing:** nnU-Net tumor segmentation + marching cubes mesh generation
- **Output:** 3D glTF mesh for Three.js visualization
- **Target:** ≥95% Dice score on BraTS dataset, working demo on 5 cases

---

## 2. Architecture Overview

```
PATIENT MRI (NIfTI)
    ↓
DICOM LOADER (nibabel)
    ↓
SEGMENTATION (nnU-Net PyTorch)
    ↓
MESH GENERATION (marching cubes + trimesh)
    ↓
EXPORT (glTF binary format)
    ↓
THREE.JS VIEWER (WebGL rendering)
```

### 2.1 Component Details

| Layer | Tech | Role | Status |
|-------|------|------|--------|
| **0: Ingestion** | nibabel, SimpleITK | Load DICOM volumes | 🟡 Ready, needs testing |
| **1: Segmentation** | PyTorch, nnU-Net | Tumor boundary detection | 🟡 Model available, integration pending |
| **2: Mesh** | scikit-image, trimesh | 3D reconstruction | 🟡 Standard library, untested |
| **3: Export** | trimesh | glTF serialization | 🟡 Standard, integration pending |
| **4: Visualization** | Three.js, WebGL | Browser rendering | ✅ Already working |

---

## 3. Sprint 1 Tasks Breakdown

### Week 1: Infrastructure (4–6 days)

#### Task 1: DICOM Loader Test (1–2 hours)
**Objective:** Validate nibabel can load BraTS NIfTI files reliably.

**Requirements:**
- Load .nii.gz files without corruption
- Extract metadata (shape, dtype, voxel spacing, affine)
- Handle edge cases: missing files, corrupted headers, unusual dimensions

**Success Criteria:**
- Load 5 BraTS cases without errors
- Metadata extraction correct
- No NaN or inf values

**Code:**
```python
from echo_pipeline import DicomLoader

loader = DicomLoader(verbose=True)
img, meta = loader.load('./data/brats/BraTS21_00000/BraTS21_00000_t1.nii.gz')

print(f"Shape: {meta['shape']}")
print(f"Range: [{meta['min']:.1f}, {meta['max']:.1f}]")
print(f"Voxel dims: {meta['voxel_dims']}")
```

---

#### Task 2: nnU-Net Inference Integration (2–3 hours)
**Objective:** Wire nnU-Net model for tumor segmentation.

**Requirements:**
- Download pre-trained weights from HuggingFace (`isensee/nnunet_brats`)
- Run inference on 3D brain volume
- Output segmentation mask (classes: 0=background, 1=necrotic, 2=tumor, 4=edema)

**Success Criteria:**
- Model loads without CUDA/memory errors
- Inference completes in <60 seconds per case on CPU
- Output mask has correct shape and class distribution

**Code:**
```python
from echo_pipeline import SegmentationPipeline

segmenter = SegmentationPipeline(device='cpu')
seg_mask = segmenter.segment(img)  # img from Task 1

print(f"Classes: {np.unique(seg_mask)}")
print(f"Shape: {seg_mask.shape}")
```

---

#### Task 3: Mesh Generation & Export (1–2 hours)
**Objective:** Convert segmentation mask to 3D mesh and export as glTF.

**Requirements:**
- Marching cubes algorithm (scikit-image)
- Vertex/face generation
- glTF binary (.glb) export with proper transformation
- Validate mesh topology (no degenerate faces)

**Success Criteria:**
- Mesh generated without topology errors
- Vertices and faces have correct shape
- glTF file loads in Three.js without errors
- File size reasonable (<50MB for full brain)

**Code:**
```python
from echo_pipeline import MeshGenerator

mesh_gen = MeshGenerator(verbose=True)
vertices, faces = mesh_gen.generate(seg_mask)
mesh_gen.export_gltf(vertices, faces, './output/brain.glb')
```

---

#### Task 4: Three.js Integration (1–2 hours)
**Objective:** Load generated mesh in browser, test rendering.

**Requirements:**
- GLTFLoader correctly loads .glb files
- Mesh renders in WebGL scene
- 360° rotation, lighting, material properties work
- Performance acceptable (60fps on desktop)

**Success Criteria:**
- Mesh visible in browser viewport
- Rotation/zoom controls functional
- No WebGL errors in console
- Frame rate stable at 60fps

**Code (React component):**
```jsx
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

export default function BrainViewer({ meshPath }) {
  useEffect(() => {
    const loader = new GLTFLoader();
    loader.load(meshPath, (gltf) => {
      scene.add(gltf.scene);
      // Set lighting, camera, controls
    });
  }, [meshPath]);
  
  return <canvas ref={mountPoint} />;
}
```

---

#### Task 5: End-to-End Demo (2–3 hours)
**Objective:** Execute full pipeline on 5 BraTS cases, validate outputs.

**Requirements:**
- Process complete: DICOM → segment → mesh → export → render
- All 5 demo cases work without errors
- Screenshots/video of visualization
- Metrics logged (processing time, mesh quality)

**Success Criteria:**
- All 5 cases processed successfully
- Dice scores logged (target: ≥0.85 per case)
- Demo video ready (5 meshes rotating, lighting demo)
- Execution time <2 hours for 5 cases on CPU

---

### Week 2: Validation & Testing (2–3 days)

#### Task 6: Full BraTS Validation (4–6 hours)
**Objective:** Run pipeline on 100 BraTS cases, compute aggregate metrics.

**Requirements:**
- Process first 100 BraTS cases
- Compute Dice score per case
- Aggregate statistics: mean, median, std, min, max
- Identify failure cases (Dice <0.70)

**Success Criteria:**
- Mean Dice ≥0.92 (nnU-Net baseline: 92.9%)
- <5 failure cases in 100
- Processing time <8 hours on CPU

**Code:**
```python
from pathlib import Path
from echo_pipeline import EchoPipeline

pipeline = EchoPipeline(device='cpu', verbose=True)
results_all = []

brats_dir = Path('./data/brats')
for case_dir in sorted(brats_dir.glob('BraTS21_*'))[:100]:
    img_path = case_dir / f'{case_dir.name}_t1.nii.gz'
    seg_path = case_dir / f'{case_dir.name}_seg.nii.gz'
    
    results = pipeline.process(str(img_path), str(seg_path))
    results_all.append(results)

# Aggregate metrics
dice_scores = [r['metrics']['dice'] for r in results_all if 'dice' in r['metrics']]
print(f"Mean Dice: {np.mean(dice_scores):.4f}")
print(f"Median Dice: {np.median(dice_scores):.4f}")
print(f"Std Dice: {np.std(dice_scores):.4f}")
```

---

#### Task 7: Error Analysis & Documentation (2–3 hours)
**Objective:** Analyze failure cases, document edge cases and mitigations.

**Requirements:**
- Identify cases with low Dice scores (<0.70)
- Categorize failures: small tumors, artifacts, segmentation errors
- Document edge cases discovered
- Create mitigation strategies for Phase 2

**Output:**
Document: `SPRINT1_ERROR_ANALYSIS.md` with:
- Failed case list (case ID, Dice, reason)
- Statistics (% failures, severity distribution)
- Recommended fixes (pre/post-processing, model tuning)

---

#### Task 8: Documentation & Demo Ready (3–4 hours)
**Objective:** Finalize technical documentation, prepare presentation materials.

**Requirements:**
- Update README with setup instructions
- Document API (function signatures, parameters, returns)
- Create demo video (5 meshes, different viewing angles)
- Write architecture diagram

**Deliverables:**
- `README.md` (setup, usage, API)
- `ARCHITECTURE.md` (component diagram, data flow)
- `METRICS.md` (Dice scores, timing, hardware specs)
- `DEMO_VIDEO.mp4` (5 cases, 60 seconds)

---

## 4. Testing Strategy

### Unit Tests
- DICOM loader: file handling, metadata extraction, validation
- Segmentation: output shape, class distribution
- Mesh generation: vertex/face correctness, export format
- Pipeline: end-to-end processing, error handling

### Integration Tests
- Full pipeline on sample mock BraTS case
- Parametrized tests on multiple cases
- Three.js visualization validation

### Validation Tests
- Dice score on ground truth (target: ≥0.85 per case)
- Mesh quality (no degenerate faces, proper topology)
- Performance benchmarks (processing time, memory usage)

**Run tests:**
```bash
pytest tests_echo_pipeline.py -v --cov=echo_pipeline
```

---

## 5. Dependencies & Setup

### Python Environment
```bash
python -m venv echo-oncology-venv
source echo-oncology-venv/bin/activate

# Core ML stack
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install transformers huggingface-hub

# Medical imaging
pip install nibabel SimpleITK scikit-image trimesh open3d

# Testing & quality
pip install pytest pytest-cov black flake8 mypy
```

### BraTS Dataset
Download from: https://www.synapse.org/#!Synapse:syn25829067
- **Size:** ~6.5GB
- **Cases:** 2,251 (training), 570 (validation)
- **Structure:**
  ```
  data/brats/
    BraTS21_00000/
      BraTS21_00000_t1.nii.gz          (T1-weighted MRI)
      BraTS21_00000_t1ce.nii.gz        (T1 contrast-enhanced)
      BraTS21_00000_t2.nii.gz          (T2-weighted MRI)
      BraTS21_00000_flair.nii.gz       (FLAIR)
      BraTS21_00000_seg.nii.gz         (Ground truth segmentation)
  ```

### Model Download
```python
from transformers import AutoModel
model = AutoModel.from_pretrained(
    'isensee/nnunet_brats',
    cache_dir='./models'
)
```

---

## 6. Success Criteria & KPIs

| KPI | Target | Measurement |
|-----|--------|-------------|
| **Dice Score (Mean)** | ≥0.92 | Validation on 100 BraTS cases |
| **Dice Score (Median)** | ≥0.93 | Robustness metric |
| **Failure Rate** | <5% | Cases with Dice <0.70 |
| **Processing Time** | <8 hrs/100 cases | CPU execution |
| **Memory Usage** | <4GB | Peak memory per case |
| **Mesh Quality** | 100% valid | No degenerate faces |
| **Demo Readiness** | 5/5 cases | Working visualization |

---

## 7. Risk & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|-----------|
| BraTS download fails | Sprint blocked | Low | Have backup dataset (ACDC, institutional) |
| nnU-Net inference slow | Performance issues | Low | Use quantization/ONNX if needed |
| Mesh generation fails | Cannot visualize | Low | Implement fallback (voxel rendering) |
| GPU not available | Extended timeline | Low | Optimize for CPU (batch processing) |
| Ground truth mismatch | Metrics unreliable | Low | Validate format against nnU-Net paper |

---

## 8. Timeline & Milestones

- **Day 1–2:** Tasks 1–3 (DICOM, segmentation, mesh)
- **Day 3:** Task 4 (Three.js integration) + Task 5 (demo on 5 cases)
- **Day 4–5:** Task 6 (100-case validation)
- **Day 6:** Task 7 (error analysis) + Task 8 (documentation)

**Weekly Sync:** Mondays 9 AM Sydney time

---

## 9. Phase 2 Context

After Sprint 1 completes:
- **Weeks 3–6:** Radiomics publication (full BraTS validation, manuscript)
- **Weeks 7–12:** Surgeon usability study (trajectory planning UI, feedback)
- **Weeks 13–24:** Regulatory pathway (IRB, FDA Class II confirmation)

---

## 10. References

- nnU-Net Paper: https://arxiv.org/abs/1904.08128
- BraTS Challenge: https://www.med.upenn.edu/cbica/brats/
- Three.js Documentation: https://threejs.org/docs/
- Marching Cubes Algorithm: https://en.wikipedia.org/wiki/Marching_cubes

---

**Last Updated:** May 29, 2026  
**Next Review:** June 5, 2026 (end of Week 1)
