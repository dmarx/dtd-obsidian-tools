# tests/test_graph.py - Test graph construction functionality

import networkx as nx
import pytest
from pathlib import Path
from obsidian.graph import build_graph, get_link_statistics, find_candidates
from obsidian.parser import ObsDoc


def test_build_graph_empty():
    """Test graph building with empty corpus."""
    corpus = []
    graph = build_graph(corpus)
    assert len(graph.nodes) == 0
    assert len(graph.edges) == 0


def test_build_graph_single_doc():
    """Test graph with single document with no links."""
    doc = ObsDoc("test", "# Test\nNo links here.")
    corpus = [doc]
    graph = build_graph(corpus)
    
    # No links means no nodes are added to the graph
    assert len(graph.nodes) == 0
    assert len(graph.edges) == 0


def test_build_graph_with_links():
    """Test graph with linked documents."""
    doc1 = ObsDoc("doc1", "# Doc1\nLinks to [[doc2]] and [[missing]].")
    doc2 = ObsDoc("doc2", "# Doc2\nLinks to [[doc1]].")
    corpus = [doc1, doc2]
    
    graph = build_graph(corpus)
    
    # Should have 3 nodes: doc1, doc2, missing (phantom)
    assert len(graph.nodes) == 3
    assert "doc1" in graph.nodes
    assert "doc2" in graph.nodes
    assert "missing" in graph.nodes
    
    # Check existence attributes
    assert graph.nodes["doc1"]["exists"] is True
    assert graph.nodes["doc2"]["exists"] is True
    assert graph.nodes["missing"]["exists"] is False
    
    # Check edges
    assert graph.has_edge("doc1", "doc2")
    assert graph.has_edge("doc1", "missing")
    assert graph.has_edge("doc2", "doc1")


def test_get_link_statistics():
    """Test link and tag statistics calculation."""
    doc1 = ObsDoc("doc1", """---
tags: [python, test]
---
# Doc1
Links to [[doc2]].""")
    
    doc2 = ObsDoc("doc2", """---
tags: [python, example]
---
# Doc2
Links to [[doc1]] and [[doc2]].""")
    
    corpus = [doc1, doc2]
    tags, indegree = get_link_statistics(corpus)
    
    # Tag counts
    assert tags["python"] == 2
    assert tags["test"] == 1
    assert tags["example"] == 1
    
    # Link counts (indegree)
    assert indegree["doc2"] == 2  # linked from doc1 and doc2
    assert indegree["doc1"] == 1  # linked from doc2


def test_find_candidates():
    """Test finding missing documents."""
    doc1 = ObsDoc("existing", "# Existing\nLinks to [[missing1]] and [[missing2]].")
    corpus = [doc1]
    
    graph = build_graph(corpus)
    candidates = find_candidates(graph)
    
    assert "missing1" in candidates
    assert "missing2" in candidates
    assert "existing" not in candidates
    
    # Each missing doc should have degree 1
    assert candidates["missing1"] == 1
    assert candidates["missing2"] == 1