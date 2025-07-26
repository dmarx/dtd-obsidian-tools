# tests/test_integration.py - Basic integration tests

import tempfile
from pathlib import Path

import pytest

from obsidian import ObsDoc, build_graph, load_corpus


def test_load_corpus_empty_directory():
    """Test loading corpus from empty directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        vault_path = Path(tmpdir)
        corpus = load_corpus(vault_path)
        assert len(corpus) == 0


def test_load_corpus_with_files():
    """Test loading corpus with markdown files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        vault_path = Path(tmpdir)

        # Create test files
        (vault_path / "doc1.md").write_text("# Document 1")
        (vault_path / "doc2.md").write_text("# Document 2")
        (vault_path / "not_markdown.txt").write_text("Not a markdown file")

        corpus = load_corpus(vault_path)

        # Should only load .md files
        assert len(corpus) == 2
        assert all(isinstance(doc, ObsDoc) for doc in corpus)
        titles = [doc.title for doc in corpus]
        assert "doc1" in titles
        assert "doc2" in titles


def test_full_workflow():
    """Test complete workflow from corpus loading to graph building."""
    with tempfile.TemporaryDirectory() as tmpdir:
        vault_path = Path(tmpdir)

        # Create interconnected documents
        (vault_path / "home.md").write_text(
            """---
title: Home Page
tags: [index, main]
---
# Welcome
See [[Projects]] and [[Ideas]]."""
        )

        (vault_path / "projects.md").write_text(
            """---
title: Projects
tags: [work]
---
# My Projects
Back to [[Home Page]]."""
        )

        (vault_path / "ideas.md").write_text(
            """---
title: Ideas
tags: [creative, brainstorm]
---
# Random Ideas
Link to [[Projects]] and [[Home Page]]."""
        )

        # Load and process
        corpus = load_corpus(vault_path)
        graph = build_graph(corpus)

        # Verify corpus
        assert len(corpus) == 3

        # Verify graph structure
        assert len(graph.nodes) >= 3
        assert "home page" in graph.nodes
        assert "projects" in graph.nodes
        assert "ideas" in graph.nodes

        # Verify connections
        assert graph.has_edge("home page", "projects")
        assert graph.has_edge("home page", "ideas")
        assert graph.has_edge("projects", "home page")
        assert graph.has_edge("ideas", "projects")
        assert graph.has_edge("ideas", "home page")

        # Verify node attributes
        for title in ["home page", "projects", "ideas"]:
            assert graph.nodes[title]["exists"] is True
