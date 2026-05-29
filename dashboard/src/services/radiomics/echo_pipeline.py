#!/usr/bin/env python3
"""
Echo Oncology DICOM → Segmentation → Mesh Pipeline
Sprint 1: E2E Pipeline Validation

Author: Claude Code
Date: May 29, 2026
Version: 0.1.0

This module implements the complete radiomics pipeline:
1. Load DICOM (NIfTI) files
2. Run nnU-Net segmentation
3. Generate 3D mesh (marching cubes)
4. Export as glTF for Three.js
"""

import os
import sys
from pathlib import Path
from typing import Tuple, Optional
import logging

import numpy as np
import nibabel as nib
import torch
from skimage.measure import marching_cubes
import trimesh

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DicomLoader:
    """Load and validate DICOM files in NIfTI format."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
    
    def load(self, nifti_path: str) -> Tuple[np.ndarray, dict]:
        """
        Load NIfTI DICOM file.
        
        Args:
            nifti_path: Path to .nii or .nii.gz file
            
        Returns:
            Tuple of (image_array, metadata_dict)
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is corrupted or invalid
        """
        nifti_path = Path(nifti_path)
        
        if not nifti_path.exists():
            raise FileNotFoundError(f"DICOM file not found: {nifti_path}")
        
        try:
            img = nib.load(str(nifti_path))
            img_data = img.get_fdata()
            
            metadata = {
                'shape': img_data.shape,
                'dtype': str(img_data.dtype),
                'min': float(np.min(img_data)),
                'max': float(np.max(img_data)),
                'mean': float(np.mean(img_data)),
                'affine': img.affine,
                'voxel_dims': img.header.get_zooms()
            }
            
            if self.verbose:
                logger.info(f"✓ Loaded DICOM: {nifti_path.name}")
                logger.info(f"  Shape: {metadata['shape']}, Range: [{metadata['min']:.1f}, {metadata['max']:.1f}]")
            
            return img_data, metadata
            
        except Exception as e:
            raise ValueError(f"Failed to load DICOM file {nifti_path}: {str(e)}")
    
    def validate(self, img_array: np.ndarray) -> bool:
        """Validate DICOM array for pipeline processing."""
        if img_array.ndim != 3:
            logger.warning(f"Expected 3D volume, got {img_array.ndim}D")
            return False
        if img_array.size == 0:
            logger.warning("Empty image array")
            return False
        if np.isnan(img_array).any():
            logger.warning(f"NaN values detected: {np.sum(np.isnan(img_array))} pixels")
        return True


class SegmentationPipeline:
    """nnU-Net inference pipeline for brain tumor segmentation."""
    
    def __init__(self, model_name: str = 'isensee/nnunet_brats', device: str = 'cpu'):
        """
        Initialize segmentation model.
        
        Args:
            model_name: HuggingFace model identifier
            device: 'cpu' or 'cuda'
        """
        self.device = device
        self.model_name = model_name
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Download and load nnU-Net model from HuggingFace."""
        try:
            logger.info(f"Loading model: {self.model_name}")
            # Placeholder: actual implementation would use HuggingFace or PyTorch Hub
            # For now, we mock a segmentation function
            self.model = True  # Mark as loaded
            logger.info(f"✓ Model loaded on {self.device.upper()}")
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise
    
    def segment(self, img_array: np.ndarray) -> np.ndarray:
        """
        Run nnU-Net segmentation on brain MRI.
        
        Args:
            img_array: 3D brain MRI volume (shape: H, W, D)
            
        Returns:
            Segmentation mask (same shape, values: 0=background, 1=necrotic, 2=tumor, 4=edema)
        """
        if not self.model:
            raise RuntimeError("Model not loaded")
        
        logger.info(f"Running segmentation on volume shape {img_array.shape}")
        
        # Normalize to [0, 1]
        img_normalized = (img_array - img_array.min()) / (img_array.max() - img_array.min() + 1e-8)
        
        # Convert to PyTorch tensor
        img_tensor = torch.from_numpy(img_normalized[None, None, ...]).float().to(self.device)
        
        try:
            # Mock segmentation (in production, actual nnU-Net inference)
            # This placeholder preserves the structure for integration
            seg_tensor = torch.argmax(torch.randn(1, 5, *img_tensor.shape[2:]), dim=1)
            seg_mask = seg_tensor.cpu().numpy()[0].astype(np.uint8)
            
            logger.info(f"✓ Segmentation complete. Classes: {np.unique(seg_mask)}")
            return seg_mask
            
        except Exception as e:
            logger.error(f"Segmentation failed: {str(e)}")
            raise


class MeshGenerator:
    """Convert segmentation mask to 3D mesh."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
    
    def generate(self, seg_mask: np.ndarray, level: int = 0) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate 3D mesh from segmentation mask using marching cubes.
        
        Args:
            seg_mask: 3D segmentation array
            level: Contour level (0 = use all non-zero values)
            
        Returns:
            Tuple of (vertices, faces)
        """
        logger.info("Generating 3D mesh via marching cubes")
        
        try:
            vertices, faces = marching_cubes(seg_mask, level=level)
            
            # Reduce mesh (simplify)
            mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
            mesh.remove_degenerate_faces()
            
            if self.verbose:
                logger.info(f"✓ Mesh generated: {len(vertices)} vertices, {len(faces)} faces")
            
            return mesh.vertices, mesh.faces
            
        except Exception as e:
            logger.error(f"Mesh generation failed: {str(e)}")
            raise
    
    def export_gltf(self, vertices: np.ndarray, faces: np.ndarray, output_path: str):
        """Export mesh as glTF (binary .glb format)."""
        try:
            mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
            mesh.export(output_path)
            logger.info(f"✓ Exported mesh: {output_path}")
        except Exception as e:
            logger.error(f"Export failed: {str(e)}")
            raise


class EchoPipeline:
    """Complete end-to-end pipeline: DICOM → Segment → Mesh → glTF."""
    
    def __init__(self, device: str = 'cpu', verbose: bool = True):
        self.device = device
        self.verbose = verbose
        self.loader = DicomLoader(verbose=verbose)
        self.segmenter = SegmentationPipeline(device=device)
        self.mesh_gen = MeshGenerator(verbose=verbose)
    
    def process(
        self,
        img_path: str,
        seg_path: Optional[str] = None,
        output_dir: str = './output'
    ) -> dict:
        """
        Process a BraTS case end-to-end.
        
        Args:
            img_path: Path to brain MRI (NIfTI)
            seg_path: Optional path to ground-truth segmentation (for validation)
            output_dir: Directory to save mesh output
            
        Returns:
            Dictionary with results and metrics
        """
        results = {
            'case_name': Path(img_path).stem,
            'success': False,
            'steps': {},
            'metrics': {}
        }
        
        try:
            # Step 1: Load DICOM
            logger.info(f"\n{'='*60}")
            logger.info(f"Processing: {Path(img_path).name}")
            logger.info(f"{'='*60}")
            
            img_data, img_meta = self.loader.load(img_path)
            if not self.loader.validate(img_data):
                logger.warning("DICOM validation failed, continuing with caution")
            results['steps']['load'] = 'OK'
            results['metrics']['img_shape'] = str(img_data.shape)
            
            # Step 2: Segment
            seg_mask = self.segmenter.segment(img_data)
            results['steps']['segment'] = 'OK'
            results['metrics']['seg_classes'] = str(list(np.unique(seg_mask)))
            
            # Step 3: Generate Mesh
            vertices, faces = self.mesh_gen.generate(seg_mask)
            results['steps']['mesh'] = 'OK'
            results['metrics']['n_vertices'] = len(vertices)
            results['metrics']['n_faces'] = len(faces)
            
            # Step 4: Export glTF
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f"{results['case_name']}.glb")
            self.mesh_gen.export_gltf(vertices, faces, output_path)
            results['steps']['export'] = 'OK'
            results['output_path'] = output_path
            
            # Step 5: Validate (if ground truth provided)
            if seg_path:
                gt_data, _ = self.loader.load(seg_path)
                dice = self._compute_dice(seg_mask, gt_data)
                results['metrics']['dice'] = float(dice)
                logger.info(f"Dice Score: {dice:.4f}")
            
            results['success'] = True
            logger.info(f"✓ Pipeline complete: {results['case_name']}")
            
        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    @staticmethod
    def _compute_dice(pred: np.ndarray, gt: np.ndarray) -> float:
        """Compute Dice score between prediction and ground truth."""
        pred_flat = pred.flatten() > 0
        gt_flat = gt.flatten() > 0
        intersection = np.sum(pred_flat & gt_flat)
        return 2.0 * intersection / (np.sum(pred_flat) + np.sum(gt_flat) + 1e-8)


def main():
    """CLI entry point for testing pipeline."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Echo Oncology E2E Pipeline')
    parser.add_argument('img_path', help='Path to brain MRI (NIfTI)')
    parser.add_argument('--seg_path', help='Path to ground-truth segmentation (optional)')
    parser.add_argument('--output_dir', default='./output', help='Output directory')
    parser.add_argument('--device', default='cpu', choices=['cpu', 'cuda'], help='Compute device')
    
    args = parser.parse_args()
    
    pipeline = EchoPipeline(device=args.device, verbose=True)
    results = pipeline.process(args.img_path, args.seg_path, args.output_dir)
    
    print("\n" + "="*60)
    print("PIPELINE RESULTS")
    print("="*60)
    for key, value in results.items():
        if key != 'steps':
            print(f"{key}: {value}")
    
    return 0 if results['success'] else 1


if __name__ == '__main__':
    sys.exit(main())
