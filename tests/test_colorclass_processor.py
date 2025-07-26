# tests/test_colorclass_processor.py - Test colorclass processor functionality

import json
import tempfile
from pathlib import Path

import pytest

from obsidian.colorclass_processor import (
    ColorclassProcessor,
    hsl_to_rgb_int,
    strided_palette,
)
from obsidian.parser import ObsDoc


def test_hsl_to_rgb_int():
    """Test HSL to RGB integer conversion."""
    # Red (hue=0, sat=1, light=0.5)
    rgb = hsl_to_rgb_int((0.0, 1.0, 0.5))
    assert rgb == 0xFF0000  # Red

    # Blue (hue=0.67, sat=1, light=0.5)
    rgb = hsl_to_rgb_int((0.67, 1.0, 0.5))
    assert isinstance(rgb, int)
    assert 0 <= rgb <= 0xFFFFFF


def test_strided_palette():
    """Test strided color palette generation."""
    colors = strided_palette(5)
    assert len(colors) == 5
    assert all(isinstance(c, int) for c in colors)
    assert all(0 <= c <= 0xFFFFFF for c in colors)


def test_processor_init():
    """Test processor initialization."""
    processor = ColorclassProcessor()
    assert processor.config.colorclass_prefix == "colorclass"
    assert processor.config.dry_run is False


def test_list_algorithms():
    """Test algorithm listing."""
    processor = ColorclassProcessor()
    algorithms = processor.list_algorithms()
    assert isinstance(algorithms, list)
    assert "louvain" in algorithms  # Should be available in most NetworkX versions


def test_process_vault_dry_run():
    """Test vault processing in dry run mode."""
    processor = ColorclassProcessor()

    with tempfile.TemporaryDirectory() as tmpdir:
        vault_path = Path(tmpdir)

        # Create test documents
        (vault_path / "doc1.md").write_text(
            """---
title: Document 1
tags: [test]
---
# Document 1
Links to [[Document 2]]."""
        )

        (vault_path / "doc2.md").write_text(
            """---
title: Document 2
tags: [test]
---
# Document 2
Links to [[Document 1]]."""
        )

        # Process in dry run mode
        assignments = processor.process_vault(str(vault_path), dry_run=True)

        # Should return assignments without modifying files
        assert isinstance(assignments, dict)
        # Original files should be unchanged
        content1 = (vault_path / "doc1.md").read_text()
        assert "colorclass/" not in content1


def test_analyze_community_structure():
    """Test community structure analysis."""
    processor = ColorclassProcessor()

    with tempfile.TemporaryDirectory() as tmpdir:
        vault_path = Path(tmpdir)

        # Create minimal test vault
        (vault_path / "doc1.md").write_text("# Doc1\nLinks to [[doc2]].")
        (vault_path / "doc2.md").write_text("# Doc2\nLinks to [[doc1]].")

        analysis = processor.analyze_community_structure(str(vault_path))

        assert "total_documents" in analysis
        assert "clustered_documents" in analysis
        assert "total_communities" in analysis
        assert analysis["total_documents"] == 2
        assert analysis["clustered_documents"] == 2


def test_config_loading():
    """Test configuration loading with custom config."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.yml"
        config_path.write_text(
            """
colorclass_prefix: "custom"
dry_run: true
community_detection:
  algorithm: "greedy_modularity"
  min_community_size: 3
"""
        )

        processor = ColorclassProcessor(str(config_path))
        assert processor.config.colorclass_prefix == "custom"
        assert processor.config.dry_run is True
        assert processor.config.community_detection.algorithm == "greedy_modularity"
        assert processor.config.community_detection.min_community_size == 3
