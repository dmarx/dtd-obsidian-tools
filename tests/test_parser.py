# tests/test_parser.py - Test core parsing functionality

from pathlib import Path

import frontmatter
import pytest

from obsidian.parser import ObsDoc, clean_links, extract_frontmatter, get_wikilinks


def test_extract_frontmatter():
    """Test YAML frontmatter extraction using python-frontmatter."""
    doc = """---
title: Test Document
tags: [tag1, tag2]
---

# Content here
Some [[link]] content."""

    metadata, body = extract_frontmatter(doc)
    assert metadata["title"] == "Test Document"
    assert metadata["tags"] == ["tag1", "tag2"]
    assert "# Content here" in body


def test_extract_frontmatter_no_frontmatter():
    """Test document without frontmatter."""
    doc = "# Just content\nNo frontmatter here."
    metadata, body = extract_frontmatter(doc)
    assert metadata == {}
    assert body == doc


def test_get_wikilinks():
    """Test wikilink extraction."""
    text = "Here are some [[Link One]] and [[Link Two|Alias]] links."
    links = get_wikilinks(text)
    assert links == ["Link One", "Link Two|Alias"]


def test_clean_links():
    """Test link cleaning and canonicalization."""
    links = ["Link One", "Link Two|Alias", "UPPERCASE"]
    cleaned = clean_links(links)
    assert cleaned == ["link one", "link two", "uppercase"]


def test_obsdoc_creation():
    """Test ObsDoc creation and properties."""
    content = """---
title: My Document
tags: [test, example]
---

# My Document
This has a [[wikilink]] and [[Another Link|alias]].
"""

    doc = ObsDoc("test-doc", content)
    assert doc.title == "My Document"  # Should use frontmatter title
    assert doc.tags == ["test", "example"]
    assert doc.links == ["wikilink", "another link"]
    assert doc.node_name == "my document"


def test_obsdoc_no_frontmatter():
    """Test ObsDoc with no frontmatter."""
    content = "# Simple Doc\nJust content with [[a link]]."
    doc = ObsDoc("simple-doc", content)
    assert doc.title == "simple-doc"
    assert doc.tags == []
    assert doc.links == ["a link"]


def test_frontmatter_roundtrip():
    """Test that frontmatter can be read and written back correctly."""
    content = """---
title: Test
tags: [one, two]
date: 2025-01-01
---

Body content here."""

    # Parse with frontmatter
    post = frontmatter.loads(content)
    assert post.metadata["title"] == "Test"
    assert post.metadata["tags"] == ["one", "two"]
    assert post.content.strip() == "Body content here."

    # Roundtrip test
    reconstructed = frontmatter.dumps(post)
    post2 = frontmatter.loads(reconstructed)
    assert post2.metadata == post.metadata
    assert post2.content == post.content
