/**
 * Advanced Three.js Utilities for Surgical Visualization
 * 
 * - Clipping plane implementation (axial/coronal/sagittal dissection)
 * - Layer peeling with progressive opacity
 * - Safety margin color gradients
 * - 4D cardiac animation
 * - Radiomics overlay rendering
 * 
 * Author: Hermes (Claude Code)
 * Date: May 29, 2026
 * Version: 1.0.0
 */

import * as THREE from 'three';

/**
 * Clipping Plane Manager
 * Handles axial, coronal, sagittal slicing through the brain
 */
export class ClippingPlaneManager {
  scene: THREE.Scene;
  planes: THREE.Plane[];
  localPlanes: THREE.Plane[];
  renderer: THREE.WebGLRenderer;

  constructor(scene: THREE.Scene, renderer: THREE.WebGLRenderer) {
    this.scene = scene;
    this.renderer = renderer;
    
    // Initialize clipping planes
    this.planes = [
      new THREE.Plane(new THREE.Vector3(0, 0, 1), 0), // axial
      new THREE.Plane(new THREE.Vector3(0, 1, 0), 0), // coronal
      new THREE.Plane(new THREE.Vector3(1, 0, 0), 0), // sagittal
    ];

    this.localPlanes = this.planes.map(p => p.clone());

    // Enable local clipping in renderer
    this.renderer.localClippingEnabled = true;
  }

  /**
   * Update clipping plane positions
   * @param axial Z-axis position (-100 to 100)
   * @param coronal Y-axis position (-100 to 100)
   * @param sagittal X-axis position (-100 to 100)
   */
  updatePlanes(axial: number, coronal: number, sagittal: number) {
    this.planes[0].constant = -axial / 100;
    this.planes[1].constant = -coronal / 100;
    this.planes[2].constant = -sagittal / 100;

    // Apply clipping to all materials in scene
    this.scene.traverse((obj) => {
      if (obj instanceof THREE.Mesh && obj.material) {
        const materials = Array.isArray(obj.material) ? obj.material : [obj.material];
        materials.forEach((mat: THREE.Material) => {
          (mat as any).clippingPlanes = this.planes;
          (mat as any).clipIntersection = false;
        });
      }
    });
  }

  /**
   * Toggle clipping on/off
   */
  setEnabled(enabled: boolean) {
    this.scene.traverse((obj) => {
      if (obj instanceof THREE.Mesh && obj.material) {
        const materials = Array.isArray(obj.material) ? obj.material : [obj.material];
        materials.forEach((mat: THREE.Material) => {
          (mat as any).clippingPlanes = enabled ? this.planes : [];
        });
      }
    });
  }

  /**
   * Get current clipping positions
   */
  getPlanes() {
    return {
      axial: -this.planes[0].constant * 100,
      coronal: -this.planes[1].constant * 100,
      sagittal: -this.planes[2].constant * 100,
    };
  }
}

/**
 * Layer Peeling Manager
 * Progressive reveal of anatomy layers
 */
export class LayerPeelingManager {
  scene: THREE.Scene;
  layers: Map<string, THREE.Object3D[]>;
  opacityMap: Map<string, number>;

  constructor(scene: THREE.Scene) {
    this.scene = scene;
    this.layers = new Map();
    this.opacityMap = new Map();

    this.initializeLayers();
  }

  /**
   * Initialize anatomical layers
   */
  private initializeLayers() {
    const layerNames = ['skin', 'brain', 'tumor', 'motor', 'speech', 'vascular', 'dti'];
    
    layerNames.forEach((name) => {
      this.layers.set(name, []);
      this.opacityMap.set(name, 1.0);
    });

    // Categorize scene objects into layers
    this.scene.traverse((obj) => {
      if (obj instanceof THREE.Mesh) {
        const name = obj.name.toLowerCase();
        if (name.includes('brain')) {
          this.layers.get('brain')?.push(obj);
        } else if (name.includes('tumor')) {
          this.layers.get('tumor')?.push(obj);
        } else if (name.includes('motor')) {
          this.layers.get('motor')?.push(obj);
        } else if (name.includes('speech')) {
          this.layers.get('speech')?.push(obj);
        } else if (name.includes('vascular')) {
          this.layers.get('vascular')?.push(obj);
        } else if (name.includes('dti')) {
          this.layers.get('dti')?.push(obj);
        }
      }
    });
  }

  /**
   * Set opacity for a specific layer
   */
  setLayerOpacity(layerName: string, opacity: number) {
    this.opacityMap.set(layerName, Math.max(0, Math.min(1, opacity)));

    const meshes = this.layers.get(layerName);
    if (meshes) {
      meshes.forEach((mesh) => {
        if (mesh instanceof THREE.Mesh && mesh.material) {
          const materials = Array.isArray(mesh.material) ? mesh.material : [mesh.material];
          materials.forEach((mat: THREE.Material) => {
            (mat as any).opacity = opacity;
            (mat as any).transparent = true;
            (mat as any).needsUpdate = true;
          });
        }
      });
    }
  }

  /**
   * Peel layer (hide completely)
   */
  peelLayer(layerName: string) {
    this.setLayerOpacity(layerName, 0);
  }

  /**
   * Reveal layer (show completely)
   */
  revealLayer(layerName: string) {
    this.setLayerOpacity(layerName, 1);
  }

  /**
   * Progressive reveal animation
   */
  animateReveal(duration: number = 2.0) {
    const layers = ['skin', 'brain', 'tumor', 'motor', 'speech', 'vascular'];
    const stepDuration = duration / layers.length;

    let startTime = Date.now();
    let currentLayer = 0;

    const animate = () => {
      const elapsed = (Date.now() - startTime) / 1000;
      const layerProgress = elapsed / stepDuration;

      if (layerProgress < 1) {
        // Reveal current layer progressively
        this.setLayerOpacity(layers[currentLayer], layerProgress);
        requestAnimationFrame(animate);
      } else if (currentLayer < layers.length - 1) {
        // Move to next layer
        this.revealLayer(layers[currentLayer]);
        currentLayer++;
        startTime = Date.now();
        requestAnimationFrame(animate);
      }
    };

    animate();
  }

  /**
   * Get all layer opacities
   */
  getOpacities() {
    return Object.fromEntries(this.opacityMap);
  }
}

/**
 * Safety Margin Coloring System
 * Color-code tumor mesh by distance to eloquent areas
 */
export class SafetyMarginColorizer {
  /**
   * Compute per-vertex colors based on distance to eloquent area
   */
  static colorByMargin(
    geometry: THREE.BufferGeometry,
    eloquentPositions: THREE.Vector3[],
    thresholds: { safe: number; caution: number; risk: number }
  ): Uint8Array {
    const positions = geometry.attributes.position.array as Float32Array;
    const colors = new Uint8Array(positions.length);

    for (let i = 0; i < positions.length; i += 3) {
      const vertexX = positions[i];
      const vertexY = positions[i + 1];
      const vertexZ = positions[i + 2];

      // Find minimum distance to any eloquent area
      let minDistance = Infinity;
      eloquentPositions.forEach((eloquentPos) => {
        const dx = vertexX - eloquentPos.x;
        const dy = vertexY - eloquentPos.y;
        const dz = vertexZ - eloquentPos.z;
        const distance = Math.sqrt(dx * dx + dy * dy + dz * dz);
        minDistance = Math.min(minDistance, distance);
      });

      // Assign color based on distance
      let r = 0, g = 0, b = 0;

      if (minDistance > thresholds.safe) {
        // Green: safe
        r = 51; g = 204; b = 51;
      } else if (minDistance > thresholds.caution) {
        // Yellow: caution
        r = 255; g = 204; b = 0;
      } else if (minDistance > thresholds.risk) {
        // Orange: high risk
        r = 255; g = 102; b = 0;
      } else {
        // Red: extreme risk
        r = 255; g = 0; b = 0;
      }

      colors[i] = r;
      colors[i + 1] = g;
      colors[i + 2] = b;
    }

    return colors;
  }

  /**
   * Create gradient material with safety margin coloring
   */
  static createSafetyMaterial(): THREE.MeshStandardMaterial {
    return new THREE.MeshStandardMaterial({
      vertexColors: true,
      metalness: 0.2,
      roughness: 0.6,
      side: THREE.DoubleSide,
      wireframe: false,
      flatShading: false,
    });
  }
}

/**
 * Radiomics Overlay Renderer
 * Display tumor heterogeneity, infiltration zones, etc.
 */
export class RadiomicsOverlay {
  /**
   * Create infiltration zone visualization
   */
  static createInfiltrationZone(centerPosition: THREE.Vector3, radius: number, infiltrationIndex: number): THREE.Mesh {
    const geometry = new THREE.SphereGeometry(radius * (1 + infiltrationIndex * 0.3), 32, 32);
    
    const material = new THREE.MeshStandardMaterial({
      color: new THREE.Color().setHSL(0.1 * infiltrationIndex, 1, 0.5),
      emissive: new THREE.Color().setHSL(0.1 * infiltrationIndex, 0.8, 0.3),
      transparent: true,
      opacity: 0.3 + infiltrationIndex * 0.2,
      metalness: 0.1,
      roughness: 0.8,
    });

    const mesh = new THREE.Mesh(geometry, material);
    mesh.position.copy(centerPosition);
    mesh.name = 'infiltration-zone';

    return mesh;
  }

  /**
   * Add heterogeneity map to tumor surface
   */
  static applyHeterogeneityMap(geometry: THREE.BufferGeometry, heterogeneityData: number[]): Uint8Array {
    const colors = new Uint8Array(heterogeneityData.length * 3);

    heterogeneityData.forEach((value, index) => {
      // Normalize value (0-1) to color
      const hue = 0.1 + (1 - value) * 0.3; // Red for high heterogeneity, green for low
      const saturation = value;
      const lightness = 0.4 + value * 0.2;

      const color = new THREE.Color().setHSL(hue, saturation, lightness);
      colors[index * 3] = Math.floor(color.r * 255);
      colors[index * 3 + 1] = Math.floor(color.g * 255);
      colors[index * 3 + 2] = Math.floor(color.b * 255);
    });

    return colors;
  }
}

/**
 * Cardiac 4D Animation System
 * Animate heart through cardiac cycle phases
 */
export class CardiacAnimator {
  geometry: THREE.BufferGeometry;
  originalPositions: Float32Array;
  isAnimating: boolean;
  phase: number; // 0-100

  constructor(geometry: THREE.BufferGeometry) {
    this.geometry = geometry;
    this.originalPositions = (geometry.attributes.position.array as Float32Array).slice();
    this.isAnimating = false;
    this.phase = 0;
  }

  /**
   * Animate to specific cardiac phase
   * 0-25: diastole (relaxed)
   * 25-50: early systole (contraction)
   * 50-75: mid systole (peak contraction)
   * 75-100: late systole (ejection)
   */
  setPhase(phase: number) {
    this.phase = Math.max(0, Math.min(100, phase));
    this.updateGeometry();
  }

  /**
   * Update geometry based on cardiac phase
   */
  private updateGeometry() {
    const positions = this.geometry.attributes.position.array as Float32Array;
    const phases = this.originalPositions;

    const t = this.phase / 100; // 0-1

    // Compute deformation based on phase
    // Diastole: full size, normal shape
    // Systole: contracted, apex moves

    for (let i = 0; i < positions.length; i += 3) {
      const x = phases[i];
      const y = phases[i + 1];
      const z = phases[i + 2];

      // Apex point (around z = -50)
      const isApex = z < -30;
      const distance = Math.sqrt(x * x + y * y + z * z);

      let contractFactor = 1.0;

      if (this.phase < 25) {
        // Diastole: no contraction
        contractFactor = 1.0;
      } else if (this.phase < 50) {
        // Early systole: 0-100% contraction
        contractFactor = 1.0 - ((this.phase - 25) / 25) * 0.2;
      } else if (this.phase < 75) {
        // Mid systole: peak contraction 100%
        contractFactor = 0.8 - ((this.phase - 50) / 25) * 0.1;
      } else {
        // Late systole: relaxing back
        contractFactor = 0.7 + ((this.phase - 75) / 25) * 0.3;
      }

      // Apply contraction (move toward center)
      positions[i] = x * contractFactor;
      positions[i + 1] = y * contractFactor;
      positions[i + 2] = isApex ? z * (contractFactor + 0.1) : z * contractFactor;
    }

    (this.geometry.attributes.position as THREE.BufferAttribute).needsUpdate = true;
  }

  /**
   * Auto-animate cardiac cycle
   */
  autoAnimate(duration: number = 1.0) {
    this.isAnimating = true;
    const startTime = Date.now();

    const animate = () => {
      const elapsed = (Date.now() - startTime) / 1000;
      const phase = (elapsed % duration) / duration * 100;

      this.setPhase(phase);

      if (this.isAnimating) {
        requestAnimationFrame(animate);
      }
    };

    animate();
  }

  /**
   * Stop animation
   */
  stopAnimation() {
    this.isAnimating = false;
  }

  /**
   * Get current phase name
   */
  getPhaseName(): string {
    if (this.phase < 25) return 'Diastole (Filling)';
    if (this.phase < 50) return 'Early Systole (Contraction)';
    if (this.phase < 75) return 'Mid Systole (Ejection)';
    return 'Late Systole (Relaxation)';
  }
}

/**
 * ECG Waveform Renderer
 * Display ECG trace synchronized with cardiac animation
 */
export class ECGRenderer {
  canvas: HTMLCanvasElement;
  ctx: CanvasRenderingContext2D;
  waveformData: number[];
  phase: number;

  constructor(canvasElement: HTMLCanvasElement, waveformData: number[] = []) {
    this.canvas = canvasElement;
    this.ctx = canvasElement.getContext('2d')!;
    this.waveformData = waveformData.length > 0 ? waveformData : this.generateSampleECG();
    this.phase = 0;
  }

  /**
   * Generate sample ECG waveform
   */
  private generateSampleECG(): number[] {
    const ecg: number[] = [];
    const samples = 500;

    for (let i = 0; i < samples; i++) {
      const t = i / samples;
      let value = 0;

      // P wave
      if (t < 0.1) {
        value = Math.sin(t * Math.PI * 10) * 0.2;
      }
      // QRS complex
      else if (t < 0.25) {
        const qrs = (t - 0.1) / 0.15;
        value = Math.sin(qrs * Math.PI * 3) * 0.8;
      }
      // T wave
      else if (t < 0.4) {
        const tw = (t - 0.25) / 0.15;
        value = Math.sin(tw * Math.PI * 2) * 0.3;
      }
      // Baseline
      else {
        value = (Math.random() - 0.5) * 0.1;
      }

      ecg.push(value);
    }

    return ecg;
  }

  /**
   * Render ECG waveform
   */
  render(phase: number) {
    this.phase = phase / 100; // 0-1

    const { width, height } = this.canvas;
    const centerY = height / 2;
    const gridColor = '#333333';
    const waveColor = '#00ff00';
    const highlightColor = '#ff0000';

    // Clear canvas
    this.ctx.fillStyle = '#000000';
    this.ctx.fillRect(0, 0, width, height);

    // Draw grid
    this.ctx.strokeStyle = gridColor;
    this.ctx.lineWidth = 0.5;

    for (let i = 0; i < width; i += 20) {
      this.ctx.beginPath();
      this.ctx.moveTo(i, 0);
      this.ctx.lineTo(i, height);
      this.ctx.stroke();
    }

    for (let i = 0; i < height; i += 20) {
      this.ctx.beginPath();
      this.ctx.moveTo(0, i);
      this.ctx.lineTo(width, i);
      this.ctx.stroke();
    }

    // Draw waveform
    this.ctx.strokeStyle = waveColor;
    this.ctx.lineWidth = 2;
    this.ctx.beginPath();

    for (let i = 0; i < this.waveformData.length; i++) {
      const x = (i / this.waveformData.length) * width;
      const y = centerY - this.waveformData[i] * (height / 3);

      if (i === 0) {
        this.ctx.moveTo(x, y);
      } else {
        this.ctx.lineTo(x, y);
      }
    }

    this.ctx.stroke();

    // Draw phase indicator
    const phaseX = this.phase * width;
    this.ctx.strokeStyle = highlightColor;
    this.ctx.lineWidth = 2;
    this.ctx.beginPath();
    this.ctx.moveTo(phaseX, 0);
    this.ctx.lineTo(phaseX, height);
    this.ctx.stroke();

    // Draw phase label
    this.ctx.fillStyle = highlightColor;
    this.ctx.font = 'bold 12px monospace';
    this.ctx.fillText(`${(this.phase * 100).toFixed(0)}%`, phaseX + 5, 20);
  }
}

export default {
  ClippingPlaneManager,
  LayerPeelingManager,
  SafetyMarginColorizer,
  RadiomicsOverlay,
  CardiacAnimator,
  ECGRenderer,
};
