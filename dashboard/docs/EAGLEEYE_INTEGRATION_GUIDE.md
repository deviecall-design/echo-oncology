# EagleEye Interactive 3D/4D Integration Guide

**Status:** Ready to integrate  
**Files:** 2 (React component + utilities)  
**Time to integrate:** 2-3 hours  
**Dependencies:** Three.js (already in your project)

---

## 📦 Files Provided

### 1. `EagleEyeInteractive3D.tsx` (React Component)
**Main interactive 3D viewer** with all features:
- ✅ Free orbit + focus on tumor
- ✅ Tumor click → radiomics popup
- ✅ Safety margin color coding (green/yellow/orange/red)
- ✅ Clipping planes (axial/coronal/sagittal dissection)
- ✅ Layer peeling (cortex opacity slider)
- ✅ Dynamic surgical lighting
- ✅ Radiomics overlay on hover
- ✅ Cardiac 4D animation (if applicable)

**Component Interface:**
```tsx
<EagleEyeInteractive3D caseData={{
  tumorVolume: 45,
  grade: 4,
  gradeConfidence: 0.93,
  safetyMargins: 4,
  infiltrationIndex: 0.82,
  distanceMotor: 8,
  distanceSpeech: 12,
  gtrProbability: 0.78,
  recurrenceRisk: 0.74,
  classification: 'Glioblastoma IDH-wildtype',
  fmriData: {...},
  dtiData: {...},
  isCardiac: false,
}} />
```

### 2. `SurgicalVisualizationUtils.ts` (Advanced Features)
Utility classes for professional-grade functionality:
- `ClippingPlaneManager` — axial/coronal/sagittal slicing
- `LayerPeelingManager` — progressive anatomical reveal
- `SafetyMarginColorizer` — distance-based coloring
- `RadiomicsOverlay` — infiltration zones + heterogeneity
- `CardiacAnimator` — 4D heart animation
- `ECGRenderer` — ECG waveform sync

---

## 🚀 Quick Integration (3 Steps)

### Step 1: Copy Files to Your Project

```bash
# Copy React component
cp /tmp/EagleEyeInteractive3D.tsx src/components/

# Copy utilities
cp /tmp/SurgicalVisualizationUtils.ts src/lib/
```

### Step 2: Update Your Page Component

If you're currently using a static viewer, replace it:

**Before:**
```tsx
// Old static viewer
export default function CasePage() {
  return <StaticBrainViewer caseData={caseData} />;
}
```

**After:**
```tsx
import EagleEyeInteractive3D from '@/components/EagleEyeInteractive3D';

export default function CasePage() {
  return <EagleEyeInteractive3D caseData={caseData} />;
}
```

### Step 3: Install Dependencies (if not present)

```bash
npm install three
# or
yarn add three
```

---

## 📋 Feature Breakdown

### 1. Free Orbit Controls
- **Mouse drag:** Rotate brain 360°
- **Mouse wheel:** Zoom in/out
- **Right-click drag:** Pan view

### 2. Tumor Interaction
- **Click tumor:** Radiomics panel appears with:
  - Grade + confidence
  - Volume, safety margins
  - Infiltration index
  - GTR probability
  - Recurrence risk
  - Eloquent area distances
- **Hover tumor:** Cursor changes to pointer, glow effect
- **"Focus Tumor" button:** Camera animates to tumor

### 3. Safety Margin Coloring
**Automatic per-vertex coloring:**
- 🟢 **Green** (>10mm from eloquent) = SAFE
- 🟡 **Yellow** (5-10mm) = CAUTION
- 🟠 **Orange** (2-5mm) = HIGH RISK
- 🔴 **Red** (<2mm) = EXTREME (likely unresectable)

*Color updates in real-time as you move clipping planes*

### 4. Clipping Planes (Dissection Mode)
Three independent sliders:
- **Axial** — slice from top/bottom (reveal tumor interior from above)
- **Coronal** — slice front-to-back (reveal tumor relationship to eloquent areas)
- **Sagittal** — slice left-to-right (reveal vascular involvement)

*Meshes behind each plane are hidden (clipping effect)*

### 5. Layer Peeling
Control opacity of 6 anatomical layers:
- **Brain** — whole brain outline
- **Tumor** — primary lesion
- **Motor Cortex** — motor area (blue)
- **Speech Area** — Broca's/Wernicke's (purple)
- **Vascular** — arteries/veins (optional)
- **DTI** — white matter tracts (optional)

*Useful workflow:*
1. Hide brain (cortex opacity 0%) → see tumor + eloquent areas clearly
2. Fade motor cortex (50%) → see tumor-motor relationship
3. Show DTI → see if resection would damage language tracts

### 6. Surgical Lighting
**Light angle slider (0-360°):** Rotate surgical lamp to reveal surface depth
- Helps identify tumor boundaries
- Shows infiltration patterns
- Mimics OR lighting

### 7. Radiomics Overlay
**On click, shows:**
- Infiltration index (0-1, higher = more spread)
- Edema volume (if DTI available)
- Risk zones (motor, speech, vascular proximity)

**On hover eloquent area:**
- Tooltip: "Primary Motor Cortex (8mm away)"
- Color changes to highlight region
- Cursor changes to crosshair

### 8. Cardiac 4D Animation (If Applicable)
For cardiac cases (Ember integration):
- **Phase slider** — manually scrub through cardiac cycle
- **4 visible phases:**
  1. Diastole (relaxed, filling)
  2. Early Systole (contraction begins)
  3. Mid Systole (peak contraction)
  4. Late Systole (ejection, relaxing)
- **ECG waveform** below canvas shows current phase

---

## 🎨 Customization

### Change Color Scheme
Edit safety margin colors in `EagleEyeInteractive3D.tsx`, around line 180:

```typescript
if (normalizedDistance > 0.7) {
  // Green: safe
  r = 0.2; g = 0.9; b = 0.2;
} else if (normalizedDistance > 0.5) {
  // Yellow: caution
  r = 0.9; g = 0.9; b = 0.2;
// ... etc
```

### Adjust Clipping Plane Sensitivity
Default range is -100 to 100. To use finer control, change in left panel:

```tsx
<input
  type="range"
  min="-100"  // Change to -200 for finer control
  max="100"
  // ...
/>
```

### Change Lighting Intensity
Modify ambient/directional light in `loadBrainMesh()`:

```typescript
const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);  // <- change 0.4
const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8); // <- change 0.8
```

### Add More Eloquent Areas
In `loadFMRIOverlay()`, add more spheres:

```typescript
// Visual field area (yellow)
const visualGeometry = new THREE.SphereGeometry(18, 16, 16);
const visualMaterial = new THREE.MeshStandardMaterial({
  color: 0xffff00,
  emissive: 0xcccc00,
  // ...
});
const visualMesh = new THREE.Mesh(visualGeometry, visualMaterial);
visualMesh.position.set(0, -30, 50);
visualMesh.name = 'visual';
scene.add(visualMesh);
```

---

## 🔧 Advanced Usage (With Utilities)

If you want to use the advanced features, import the utilities:

```tsx
import {
  ClippingPlaneManager,
  LayerPeelingManager,
  CardiacAnimator,
  ECGRenderer,
} from '@/lib/SurgicalVisualizationUtils';

// In your component:
const clippingManager = new ClippingPlaneManager(scene, renderer);
clippingManager.updatePlanes(30, -20, 15);

const layerManager = new LayerPeelingManager(scene);
layerManager.animateReveal(2.0); // 2-second animation

const cardiac = new CardiacAnimator(heartGeometry);
cardiac.autoAnimate(1.0); // 1-second heartbeat
```

---

## 📊 Data Requirements

Your `caseData` object must include:

```typescript
interface CaseData {
  // Tumor metrics
  tumorVolume: number;           // cm³
  grade: number;                 // 2, 3, or 4
  gradeConfidence: number;       // 0-1
  safetyMargins: number;         // mm
  infiltrationIndex: number;     // 0-1
  gtrProbability: number;        // 0-1
  recurrenceRisk: number;        // 0-1
  classification: string;        // "Glioblastoma IDH-wildtype"

  // Eloquent area distances (mm)
  distanceMotor: number;
  distanceSpeech: number;

  // Optional: fMRI/DTI data
  fmriData?: any;
  dtiData?: any;

  // Optional: cardiac flag
  isCardiac?: boolean;
}
```

If you're pulling from your BraTS cases, you already have most of this. Just map your radiomics output to this interface.

---

## ⚡ Performance Optimization

For multiple cases or high-resolution meshes:

1. **Use WebGL Level of Detail (LOD)**
   ```tsx
   import { LOD } from 'three';
   const lod = new LOD();
   lod.addLevel(detailedMesh, 0);
   lod.addLevel(simplifiedMesh, 100);
   ```

2. **Defer mesh loading**
   ```tsx
   // Load brain on render, eloquent areas on click
   ```

3. **Enable frustum culling**
   ```tsx
   renderer.sortObjects = false; // Skip depth sorting
   ```

4. **Limit clipping plane updates**
   ```tsx
   // Only update on mouse up, not every move
   canvas.addEventListener('mouseup', () => updateClippingPlanes());
   ```

---

## 🧪 Testing Checklist

Before shipping to surgeons:

- [ ] **Interaction:** Click tumor → radiomics panel appears instantly (<200ms)
- [ ] **Color:** Safety margin colors visible and change smoothly
- [ ] **Clipping:** Sliders work, mesh clips cleanly (no artifacts)
- [ ] **Layers:** Opacity sliders work independently
- [ ] **Lighting:** Angle slider reveals surface features
- [ ] **Performance:** 60fps on mid-range GPU (no stuttering)
- [ ] **Mobile:** Touch controls for pan/zoom (if needed)
- [ ] **Accessibility:** Keyboard shortcuts (arrow keys to rotate)

---

## 🐛 Common Issues & Fixes

### Issue: Tumor not showing
**Fix:** Ensure `tumorVolume` is >0 and `grade` is 2-4

### Issue: Colors look washed out
**Fix:** Increase emissiveIntensity in material:
```tsx
emissive: 0xffffff,
emissiveIntensity: 0.5, // <- increase to 0.8
```

### Issue: Clipping planes not working
**Fix:** Enable local clipping in renderer:
```tsx
renderer.localClippingEnabled = true;
```

### Issue: 3D viewer black screen
**Fix:** Check camera position and scene lighting
```tsx
camera.position.set(0, 0, 150); // Ensure not inside mesh
```

---

## 📞 Support

If you hit issues during integration:

1. **Check console** for WebGL errors
2. **Verify data format** matches CaseData interface
3. **Test with sample data** first (provided in component)
4. **Post questions** in sprint sync (Monday 9 AM Sydney)

---

## 🎯 Next Steps

1. **Week 1:** Integrate component, test on EagleEye POC with 1 case
2. **Week 2:** Test on all 15 BraTS cases, collect surgeon feedback
3. **Week 3:** Polish based on feedback, optimize performance
4. **Week 4:** Deploy to Phase 2 hospital pilot (St Vincent's, RPA, Westmead)

---

## 📈 Success Metrics

- Surgeon feedback: ≥4.5/5 usability score
- Interaction latency: <200ms click-to-panel
- Performance: 60fps on hospital OR workstations
- Adoption: >80% of surgeons using for planning by month 3

---

**Integration Status:** ✅ READY  
**Estimated Integration Time:** 2-3 hours  
**Testing Time:** 4-6 hours  
**Total:** 1 week (development + testing)

Let me know when you're ready to integrate. I can help debug or optimize if needed. 🚀
