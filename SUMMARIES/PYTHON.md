# Python Project Structure

## obsidian/colorclass_processor.py
```python
def hsl_to_rgb_int(hsl: Tuple[[float, float, float]]) -> int
    """
    Convert HSL color to RGB integer format used by Obsidian.
    Args:
        hsl: Tuple of (hue, saturation, lightness) values between 0-1
    Returns:
        RGB integer value
    """

def strided_palette(n: int, stride: int) -> list[int]
    """
    Generate a strided color palette.
    Args:
        n: Number of colors to generate.
        stride: Step size for color generation.
    Returns:
        List of strided color RGB integers.
    """

class ColorclassProcessor
    """Processes Obsidian vault to add unique colorclass tags with NetworkX community detection."""

    def __init__(self, config_path: str | None)
        """Initialize processor with optional config file."""

    def _load_config(self, config_path: str | None) -> DictConfig
        """Load configuration from YAML file or use defaults."""

    def list_algorithms(self) -> list[str]
        """List available community detection algorithms."""

    def process_vault(self, vault_path: str, dry_run: bool | None, algorithm: str | None) -> dict[[str, str]]
        """
        Process vault to add colorclass tags using community detection.
        Args:
            vault_path: Path to Obsidian vault directory
            dry_run: If True, show what would be changed without modifying files
            algorithm: Community detection algorithm to use (overrides config)
        Returns:
            Dictionary mapping article names to their assigned colorclass tags
        """

    def _generate_obsidian_graph_config(self, vault_path: Path, colorclass_to_color: dict[[str, int]]) -> None
        """Generate or update .obsidian/graph.json with colorGroups."""

    def _detect_communities(self, corpus: list['ObsDoc'], algorithm: str) -> tuple[[list[set[str]], Any]]
        """Use NetworkX community detection to assign colorclass tags."""

    def _run_networkx_algorithm(self, graph: Any, algorithm: str) -> list[set[str]]
        """Run NetworkX community detection algorithm."""

    def _recursive_kernighan_lin(self, graph: Any, params: dict[[str, Any]], max_depth: int) -> list[set[str]]
        """Apply Kernighan-Lin bisection recursively to create multiple communities."""

    def _process_communities(self, communities: list[set[str]], graph: Any) -> dict[[str, str]]
        """Process communities into colorclass assignments."""

    def _apply_assignments(self, corpus: list['ObsDoc'], vault_path: Path, assignments: dict[[str, str]]) -> int
        """Apply colorclass assignments to document files."""

    def _add_colorclass_tag(self, doc: 'ObsDoc', vault_path: Path, colorclass_tag: str) -> bool
        """
        Add colorclass tag to a document's frontmatter.
        Args:
            doc: ObsDoc instance to modify
            vault_path: Path to vault directory
            colorclass_tag: The colorclass tag to add
        Returns:
            True if file was modified, False otherwise
        """

    def analyze_community_structure(self, vault_path: str, algorithm: str | None) -> dict[[str, Any]]
        """Analyze community structure that would be detected."""


def main() -> None
    """CLI entry point for colorclass processor."""

def bisect_graph(g: Any, depth: int) -> None

```

## obsidian/graph.py
```python
def load_corpus(obs_root: Path | str) -> list[ObsDoc]
    """Load all markdown documents from vault directory."""

def build_graph(corpus: list[ObsDoc]) -> Any
    """Build directed graph from document corpus."""

def get_link_statistics(corpus: list[ObsDoc]) -> tuple[[Counter[str], Counter[str]]]
    """Calculate tag and indegree statistics."""

def find_candidates(G: Any) -> dict[[str, int]]
    """Find missing documents with their connection degrees."""

```

## obsidian/parser.py
```python
def get_wikilinks(text: str) -> list[str]
    """Extract all wikilinks from text using [[link]] pattern."""

def clean_links(wikilinks: list[str], collect_aliases: bool) -> list[str]
    """Canonicalize aliases, standardize case."""

class ObsDoc
    """Represents a single Obsidian document."""

    def __init__(self, title: str, raw: str, fpath: Path | str | None)

    @property
    def node_name(self) -> str
        """Canonicalized title for graph nodes."""

    @classmethod
    def from_path(cls, fpath: Path | str) -> 'ObsDoc'
        """Create ObsDoc from file path."""


def read_yaml(txt: str) -> dict[[str, Any]]
    """Parse YAML text and return as dictionary."""

def extract_frontmatter(doc: str) -> tuple[[dict[[str, Any]], str]]
    """Extract YAML frontmatter and body from markdown document."""

```

## tests/test_colorclass_processor.py
```python
def test_hsl_to_rgb_int()
    """Test HSL to RGB integer conversion."""

def test_strided_palette()
    """Test strided color palette generation."""

def test_processor_init()
    """Test processor initialization."""

def test_list_algorithms()
    """Test algorithm listing."""

def test_process_vault_dry_run()
    """Test vault processing in dry run mode."""

def test_analyze_community_structure()
    """Test community structure analysis."""

def test_config_loading()
    """Test configuration loading with custom config."""

```

## tests/test_graph.py
```python
def test_build_graph_empty()
    """Test graph building with empty corpus."""

def test_build_graph_single_doc()
    """Test graph with single document with no links."""

def test_build_graph_with_links()
    """Test graph with linked documents."""

def test_get_link_statistics()
    """Test link and tag statistics calculation."""

def test_find_candidates()
    """Test finding missing documents."""

```

## tests/test_integration.py
```python
def test_load_corpus_empty_directory()
    """Test loading corpus from empty directory."""

def test_load_corpus_with_files()
    """Test loading corpus with markdown files."""

def test_full_workflow()
    """Test complete workflow from corpus loading to graph building."""

```

## tests/test_parser.py
```python
def test_extract_frontmatter()
    """Test YAML frontmatter extraction using python-frontmatter."""

def test_extract_frontmatter_no_frontmatter()
    """Test document without frontmatter."""

def test_get_wikilinks()
    """Test wikilink extraction."""

def test_clean_links()
    """Test link cleaning and canonicalization."""

def test_obsdoc_creation()
    """Test ObsDoc creation and properties."""

def test_obsdoc_no_frontmatter()
    """Test ObsDoc with no frontmatter."""

def test_frontmatter_roundtrip()
    """Test that frontmatter can be read and written back correctly."""

```
