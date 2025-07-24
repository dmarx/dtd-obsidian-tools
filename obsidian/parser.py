# obsidian/parser.py - Core document parsing utilities

import re
import frontmatter
from pathlib import Path
from typing import Any


def get_wikilinks(text: str) -> list[str]:
    """Extract all wikilinks from text using [[link]] pattern."""
    links_pat = re.compile(r"\[\[(.+?)\]\]")
    return re.findall(links_pat, text)


def clean_links(wikilinks: list[str], collect_aliases: bool = False) -> list[str]:
    """Canonicalize aliases, standardize case."""
    if collect_aliases:
        raise NotImplementedError
    outv = []
    for link in wikilinks:
        if '|' in link:
            try:
                link, alias = link.split('|')
            except:
                print(link)
                raise
        outv.append(link.lower())
    return outv


class ObsDoc:
    """Represents a single Obsidian document."""
    
    def __init__(self, title: str, raw: str, fpath: Path | str | None = None):
        self.title = title
        self.raw = raw
        
        # Parse with python-frontmatter
        self.post = frontmatter.loads(raw)
        self.frontmatter = self.post.metadata
        self.body = self.post.content
        
        # Use frontmatter title if available
        if 'title' in self.frontmatter:
            self.title = self.frontmatter['title']
            
        self.links = clean_links(get_wikilinks(self.body))
        self.tags = self.frontmatter.get('tags', [])
        self.fpath = Path(fpath) if fpath else None

    @property
    def node_name(self) -> str:
        """Canonicalized title for graph nodes."""
        return self.title.lower()

    @classmethod
    def from_path(cls, fpath: Path | str) -> 'ObsDoc':
        """Create ObsDoc from file path."""
        fpath = Path(fpath)
        with fpath.open(encoding='utf-8') as f:
            try:
                return cls(fpath.stem, f.read(), fpath=fpath)
            except Exception as e:
                print(fpath)
                raise e


# Keep these for backwards compatibility
def read_yaml(txt: str) -> dict[str, Any]:
    """Parse YAML text and return as dictionary."""
    import yaml
    result = yaml.load(txt, yaml.Loader)
    return result if isinstance(result, dict) else {}


def extract_frontmatter(doc: str) -> tuple[dict[str, Any], str]:
    """Extract YAML frontmatter and body from markdown document."""
    post = frontmatter.loads(doc)
    return post.metadata, post.content
