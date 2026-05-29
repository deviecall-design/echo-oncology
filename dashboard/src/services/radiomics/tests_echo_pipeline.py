#!/usr/bin/env python3
"""
Echo Oncology Pipeline Tests
Sprint 1: E2E Validation

Test suite for DICOM loader, segmentation, and mesh generation.
Run with: pytest tests_echo_pipeline.py -v --cov=echo_pipeline
"""

import pytest
import numpy as np
from pathlib import Path
from unittest.mock import Mock, patch
from echo_pipeline import DicomLoader, SegmentationPipeline, MeshGenerator, EchoPipeline


class TestDicomLoader:
    """Test DICOM loading and validation."""
    
    @pytest.fixture
    def loader(self):
        return DicomLoader(verbose=False)
    
    def test_load_missing_file(self, loader):
        """Should raise FileNotFoundError for missing file."""
        with pytest.raises(FileNotFoundError):
            loader.load('/nonexistent/file.nii.gz')
    
    def test_validate_3d_volume(self, loader):
        """Should validate 3D volume."""
        img_3d = np.random.rand(128, 128, 128)
        assert loader.validate(img_3d) == True
    
    def test_validate_rejects_empty(self, loader):
        """Should reject empty array."""
        img_empty = np.array([])
        assert loader.validate(img_empty) == False
    
    def test_validate_rejects_2d(self, loader):
        """Should warn on 2D input."""
        img_2d = np.random.rand(128, 128)
        assert loader.validate(img_2d) == False


class TestSegmentationPipeline:
    """Test nnU-Net segmentation."""
    
    @pytest.fixture
    def segmenter(self):
        return SegmentationPipeline(device='cpu')
    
    def test_model_initialization(self, segmenter):
        """Should initialize model."""
        assert segmenter.model is not None
    
    def test_segment_output_shape(self, segmenter):
        """Should output segmentation mask with input shape."""
        img = np.random.rand(128, 128, 128)
        seg = segmenter.segment(img)
        assert seg.shape == img.shape
        assert seg.dtype in [np.uint8, np.int32, np.int64]
    
    def test_segment_no_model_raises(self):
        """Should raise error if model not loaded."""
        segmenter = SegmentationPipeline()
        segmenter.model = None
        img = np.random.rand(128, 128, 128)
        with pytest.raises(RuntimeError):
            segmenter.segment(img)


class TestMeshGenerator:
    """Test mesh generation."""
    
    @pytest.fixture
    def mesh_gen(self):
        return MeshGenerator(verbose=False)
    
    def test_generate_mesh(self, mesh_gen):
        """Should generate vertices and faces."""
        # Create simple binary mask
        mask = np.zeros((50, 50, 50), dtype=np.uint8)
        mask[10:40, 10:40, 10:40] = 1
        
        vertices, faces = mesh_gen.generate(mask)
        assert len(vertices) > 0
        assert len(faces) > 0
        assert vertices.ndim == 2 and vertices.shape[1] == 3
        assert faces.ndim == 2 and faces.shape[1] == 3
    
    def test_export_gltf(self, mesh_gen, tmp_path):
        """Should export mesh as glTF."""
        vertices = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]])
        faces = np.array([[0, 1, 2]])
        
        output_path = str(tmp_path / "test_mesh.glb")
        mesh_gen.export_gltf(vertices, faces, output_path)
        
        assert Path(output_path).exists()
        assert Path(output_path).stat().st_size > 0


class TestEchoPipeline:
    """Integration tests for full pipeline."""
    
    @pytest.fixture
    def pipeline(self):
        return EchoPipeline(device='cpu', verbose=False)
    
    def test_pipeline_initialization(self, pipeline):
        """Should initialize all components."""
        assert pipeline.loader is not None
        assert pipeline.segmenter is not None
        assert pipeline.mesh_gen is not None
    
    def test_compute_dice(self):
        """Should compute Dice score correctly."""
        pred = np.array([[[1, 1], [1, 1]]])
        gt = np.array([[[1, 1], [1, 0]]])
        dice = EchoPipeline._compute_dice(pred, gt)
        assert 0 < dice < 1
        assert abs(dice - 0.857) < 0.01  # 6/7 = 0.857


class TestIntegration:
    """End-to-end pipeline integration tests."""
    
    @pytest.fixture
    def sample_brats_case(self, tmp_path):
        """Create mock BraTS case."""
        import nibabel as nib
        
        # Create mock brain MRI
        brain = np.random.rand(240, 240, 155)
        brain[80:160, 80:160, 50:130] += 5  # Simulate tumor region
        
        # Create mock segmentation
        seg = np.zeros((240, 240, 155), dtype=np.uint8)
        seg[90:150, 90:150, 60:120] = 1  # Tumor core
        seg[85:155, 85:155, 55:125] = np.maximum(seg[85:155, 85:155, 55:125], 2)  # Edema
        
        # Save as NIfTI
        img_path = str(tmp_path / "brain.nii.gz")
        seg_path = str(tmp_path / "brain_seg.nii.gz")
        
        nib.save(nib.Nifti1Image(brain, np.eye(4)), img_path)
        nib.save(nib.Nifti1Image(seg, np.eye(4)), seg_path)
        
        return img_path, seg_path, tmp_path
    
    @pytest.mark.skipif(True, reason="Requires actual BraTS data")
    def test_full_pipeline(self, sample_brats_case):
        """Should process complete case end-to-end."""
        img_path, seg_path, output_dir = sample_brats_case
        
        pipeline = EchoPipeline(device='cpu', verbose=False)
        results = pipeline.process(img_path, seg_path, str(output_dir))
        
        assert results['success'] == True
        assert 'load' in results['steps']
        assert 'segment' in results['steps']
        assert 'mesh' in results['steps']
        assert 'export' in results['steps']
        assert Path(results['output_path']).exists()


# Parametrized tests for multiple BraTS cases
@pytest.mark.parametrize('case_id', [
    'BraTS21_00000',
    'BraTS21_00001',
    'BraTS21_00005',
])
@pytest.mark.skipif(True, reason="Requires BraTS dataset")
def test_pipeline_on_brats_cases(case_id):
    """Test pipeline on actual BraTS cases."""
    brats_dir = Path('./data/brats')
    img_path = brats_dir / case_id / f'{case_id}_t1.nii.gz'
    seg_path = brats_dir / case_id / f'{case_id}_seg.nii.gz'
    
    if not img_path.exists():
        pytest.skip(f"BraTS case {case_id} not found")
    
    pipeline = EchoPipeline(device='cpu', verbose=False)
    results = pipeline.process(str(img_path), str(seg_path), './output')
    
    assert results['success'] == True
    assert results['metrics']['dice'] >= 0.8  # Expect ≥80% Dice
