# EagleEye 3D/4D Enhancement Specification

**Project:** Echo Oncology Surgical Intelligence  
**Component:** EagleEye 3D Visualization & 4D Cardiac  
**Priority:** CRITICAL (surgeon usability dependent)  
**Status:** Spec In Progress  
**Version:** 1.0

---

## 1. Current State (Working POC)

### What Exists
- ✅ Three.js 3D brain rendering
- ✅ Case management (15 BraTS cases)
- ✅ Radiomics data display (grade, infiltration, recurrence risk)
- ✅ Static tumor visualization (yellow highlight)
- ✅ Functional mapping tabs (fMRI, DTI loaded)
- ✅ Multi-phase workflow (Pre-op, Intra-op, Post-op)

### What's Missing (3D Interaction)
- ❌ Tumor click interaction (no stats panel on click)
- ❌ Color-coding by safety margin (all yellow, no risk gradient)
- ❌ Layer peeling/dissection (no progressive reveal)
- ❌ Region toggle controls (no on/off buttons)
- ❌ Eloquent area highlighting (fMRI/DTI loaded but not visualized)
- ❌ 4D cardiac animation (for Ember integration)
- ❌ Trajectory planning UI (for Phase 2 intraoperative nav)

---

## 2. Feature Specification: 3D Enhancement

### 2.1 Tumor Interaction (Click-to-Stats)

**Requirement:** User clicks tumor → panel appears with surgical metrics

**Interaction Flow:**
```
User hovers tumor → highlight yellow (current state)
User clicks tumor → 
  1. Tumor mesh turns bright white/glow effect
  2. Right panel updates to show:
     - Volume: 45 cm³
     - Grade: IV (93% confidence)
     - Classification: Glioblastoma IDH-wildtype
     - Margins: 4mm safety corridor
     - Infiltration Index: 0.82 (high)
     - GTR Probability: 78%
     - Recurrence Risk: 74% (12-month)
     - fMRI Distance to Motor: 8mm ⚠️
     - DTI Distance to Speech: 12mm ✓
  3. Option buttons appear:
     - "Plan Trajectory"
     - "View Functional Map"
     - "Compare Grade"
```

**Technical Implementation:**
- Raycaster on Three.js scene to detect mesh intersection
- onClick handler triggers:
  - Material change (emission, brightness)
  - Panel state update (React)
  - Animation: smooth zoom to tumor (camera pan)
- Confirmation button to lock selection

---

### 2.2 Safety Margin Color Coding

**Requirement:** Tumor color changes based on proximity to eloquent areas

**Color Scheme:**
```
Green   (>10mm from eloquent) = SAFE
Yellow  (5-10mm)            = CAUTION
Orange  (2-5mm)             = HIGH RISK
Red     (<2mm)              = EXTREME (likely inoperable)
```

**Implementation:**
- Pre-compute distance field from eloquent areas (fMRI, DTI)
- Per-vertex color assignment based on distance
- Shader applies gradient coloring on render
- Legend shows color meaning

**Visual Effect:**
- Tumor rendered as gradient mesh
- Green core (safe to remove) → yellow edges (risk zone) → red boundaries (eloquent contact)
- Surgeon sees at a glance: "What can I safely remove?"

---

### 2.3 Progressive Layer Peeling (Dissection Slider)

**Requirement:** User slides to progressively reveal anatomy (like MRI slice animation)

**Layer Stack (top to bottom):**
1. **Skin/Scalp** (fade first, immediately)
2. **Brain Exterior** (gray matter outline)
3. **Tumor** (bright highlight)
4. **Eloquent Areas** (motor cortex, speech area, visual cortex)
5. **White Matter Tracts** (DTI fiber bundles)
6. **Vascular** (arteries, veins)
7. **Deep Structures** (thalamus, basal ganglia)

**Interaction:**
```
Slider at 0%   → Only skin visible (context)
Slider at 20%  → Brain outline appears
Slider at 40%  → Tumor visible
Slider at 60%  → Motor/speech areas highlighted
Slider at 80%  → White matter tracts visible
Slider at 100% → Full anatomy (vascular, deep structures)
```

**Technical Implementation:**
- Multiple mesh layers with separate opacity controls
- Slider state → opacity values per layer
- Smooth interpolation (0.2s animation per slider move)
- Keyboard shortcuts: < > to step through layers

---

### 2.4 Region Toggle Controls

**Requirement:** Buttons to show/hide specific anatomical regions

**Toggle Buttons (Left Panel):**
```
[BRAIN]    [TUMOR]    [MOTOR]    [SPEECH]    [VASCULAR]
  ✓         ✓          ✓          ✓           ✗
```

**Behavior:**
- Each button toggles on/off (click to toggle)
- Visual state: active=bright, inactive=dimmed
- When toggled on: mesh appears/highlights in scene
- When toggled off: mesh fades out (or disappears)

**Color Scheme per Region:**
- BRAIN: gray (outline only)
- TUMOR: yellow/red gradient (by safety margin)
- MOTOR: blue highlight (motor cortex activation)
- SPEECH: purple highlight (Broca's/Wernicke's area)
- VASCULAR: red/pink (arteries/veins)

**Example Workflow:**
```
Surgeon: "I only want to see tumor + motor cortex"
Action: Click [BRAIN] OFF, [TUMOR] ON, [MOTOR] ON, [SPEECH] OFF, [VASCULAR] OFF
Result: Scene shows yellow tumor with blue motor area, everything else hidden
```

---

### 2.5 Eloquent Area Visualization (fMRI/DTI Overlay)

**Requirement:** Display functional brain mapping from pre-operative imaging

**fMRI Overlay:**
- Motor cortex activation (from task-based fMRI)
- Speech area activation (language task)
- Visual field representation (if tumor near visual cortex)
- Color-code by activation strength (blue=weak, red=strong)

**DTI Overlay:**
- White matter tracts (fiber bundles)
- Corticospinal tract (motor pathway, critical for resection)
- Arcuate fasciculus (language pathway)
- Inferior fronto-occipital fasciculus (vision pathway)
- Render as semi-transparent tubes/ribbons

**Interactive Features:**
- Hover over fMRI area → tooltip shows: "Primary Motor Cortex (8mm away)"
- Click fMRI area → highlight + show statistics
- Opacity slider for fMRI/DTI independent of other layers

---

## 3. Feature Specification: 4D Enhancement (Cardiac Integration)

### 3.1 4D Cardiac Animation (Ember Integration)

**Requirement:** Beating heart visualization for cardiac surgical cases

**Current State:** Static 3D heart mesh (if applicable to cases)

**Enhancement:**
- Animate heart through cardiac cycle (systole → diastole → systole)
- 4 phases visible:
  1. **Diastole** (relaxed, full)
  2. **Early Systole** (contraction begins)
  3. **Mid Systole** (peak contraction)
  4. **Late Systole** (ejection phase)

**Animation Loop:**
- Frame 0-25: Diastole (mesh expanded)
- Frame 25-50: Early systole (mesh contracts, apex moves)
- Frame 50-75: Mid systole (peak contraction)
- Frame 75-100: Late systole → back to diastole

**Synthetic ECG Display:**
- Show ECG waveform below 3D view
- Highlight cardiac phase on ECG trace
- Timeline slider to pause/rewind animation

**Risk Score Overlay:**
- Color-code myocardium by risk zones (ejection fraction, wall motion abnormality)
- Green=normal, yellow=hypokinetic, red=akinetic

---

## 4. Diagnosis Workflow (Interactive Classification)

### 4.1 Tumor Grade Selection UI

**Current State:** Grade displayed as static metric (e.g., "Grade IV 93%")

**Enhancement:**
```
Click tumor → Right panel shows:

[TUMOR GRADE SELECTOR]
 ○ Grade II - Diffuse Astrocytoma (IDH-mutant)
 ○ Grade II - Infiltrative Oligodendroglioma
 ● Grade IV - Glioblastoma IDH-wildtype (Selected)
 ○ Grade IV - GBM with TP53 mutation
 
[ESTIMATED OUTCOMES]
GTR Probability: 78%
New Deficits Risk: 22%
Recurrence (12-mo): 74%
```

**Interaction:**
- User can click different grade options to see outcome probability changes
- Helps surgeon plan based on tumor subtype
- Shows how grade classification impacts surgical strategy

---

## 5. Technical Architecture

### 5.1 Three.js Scene Structure

```
Scene
├── Lighting
│   ├── Ambient light (0.5 intensity)
│   ├── Directional light (surgical OR-style)
│   └── Point lights (tumor highlight)
├── Camera
│   ├── Initial position: looking at tumor
│   ├── Zoom range: 1-10x
│   └── Pan/rotate with mouse controls
├── Meshes
│   ├── Brain (gray, static)
│   ├── Tumor (dynamic color, interactive)
│   ├── Motor cortex (blue highlight, conditional)
│   ├── Speech area (purple highlight, conditional)
│   ├── Vascular (red/pink, conditional)
│   ├── DTI tracts (semi-transparent tubes, conditional)
│   └── Cardiac mesh (if applicable, animated)
└── UI Overlays
    ├── Tooltip (on hover)
    ├── Stats panel (on click)
    ├── Layer slider
    ├── Region toggle buttons
    └── Cardiac ECG display
```

### 5.2 Data Flow

```
BraTS Case
├── T1 MRI → Brain segmentation (static mesh)
├── T2 MRI → Tumor segmentation
├── Tumor label map → nnU-Net grade prediction (93% confidence)
├── fMRI → Motor/speech activation maps (distance calculation)
├── DTI → Fiber tract segmentation
└── Pre-computed metrics:
    ├── Distance field (tumor to eloquent areas)
    ├── Safety margin zones
    ├── GTR probability model
    └── Recurrence risk model
    
User Interaction
├── Click tumor → Query distance field → Update panel
├── Slide dissection → Set layer opacities
├── Toggle region → Show/hide mesh
└── Select grade → Recalculate outcome probabilities
```

### 5.3 React Component Structure

```
EagleEyeViewer
├── ThreeScene (Canvas)
│   ├── useRef(rendererRef)
│   ├── useEffect(initScene)
│   ├── useEffect(handleClick)
│   └── Raycaster for intersection detection
├── ControlPanel (Left sidebar)
│   ├── LayerSlider (dissection control)
│   ├── RegionToggles (Brain, Tumor, Motor, Speech, Vascular)
│   └── ZoomControls
├── StatsPanel (Right sidebar, conditional)
│   ├── TumorStats (volume, grade, margins)
│   ├── RiskMetrics (recurrence, GTR, deficits)
│   ├── FunctionalMapping (distance to eloquent)
│   └── ActionButtons (Plan Trajectory, Compare Grade)
└── CardiacECG (if applicable)
    ├── AnimationPhaseDisplay
    ├── ECGWaveform
    └── PlaybackControls
```

---

## 6. Success Criteria

### 3D Enhancement
- ✅ Click tumor → stats panel appears in <200ms
- ✅ Color gradient visible (green → yellow → red by safety margin)
- ✅ Layer slider works smoothly, no jank
- ✅ Region toggles on/off consistently
- ✅ fMRI/DTI overlay highlights visible when enabled
- ✅ Surgeon feedback: "I can understand tumor anatomy at a glance"

### 4D Cardiac
- ✅ Heart beats smoothly (24-30 fps on desktop)
- ✅ ECG synchronized with animation
- ✅ 4 cardiac phases clearly visible
- ✅ Risk zone color coding accurate

### Performance
- ✅ Initial load: <3 seconds (mesh + data)
- ✅ Click interaction: <200ms response
- ✅ Slider drag: smooth (no stuttering)
- ✅ Memory: <500MB peak (15 BraTS cases)
- ✅ GPU: Works on mid-range GPUs (GTX 1060+)

---

## 7. Implementation Phases

### Phase 1 (Week 1): Core Interaction
- Tumor click → stats panel
- Safety margin color coding
- Region toggle buttons
- **Effort:** 3-4 days

### Phase 2 (Week 2): Advanced Features
- Layer peeling/dissection slider
- fMRI/DTI visualization
- Cardiac 4D animation (if cardiac cases exist)
- **Effort:** 3-4 days

### Phase 3 (Week 3): Polish & Testing
- Surgeon usability testing
- Performance optimization
- Edge case handling
- **Effort:** 2-3 days

---

## 8. Blockers & Dependencies

**Blockers:**
- ❓ Are cardiac cases (Ember) in the 15 BraTS cases, or separate?
- ❓ Are fMRI/DTI data already preprocessed, or need processing?
- ❓ What's the maximum number of cases for Phase 2 hospital deployment?

**Dependencies:**
- Echo Oncology radiomics pipeline must validate Dice ≥95% (Sprint 1)
- fMRI/DTI distance computation needs atlas registration
- Cardiac animation needs synthetic ECG generation (Ember pipeline)

---

## 9. Next Steps

1. **Confirm scope:** Are all 3 features (tumor interaction, layer peeling, cardiac 4D) in Phase 1, or phased?
2. **Provide data:** fMRI/DTI preprocessing status for 15 cases
3. **Usability testing:** Which surgeons review wireframes?
4. **Timeline:** When should 3D enhancement be complete? (before surgeon usability study?)

---

**Status:** 🟡 Awaiting clarification on scope + data availability  
**Owner:** Hermes (Claude Code)  
**Stakeholder:** Damien Callaghan (Echo Oncology)

