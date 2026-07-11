from dataclasses import dataclass
from typing import Optional


@dataclass
class Finding:
    tool: str
    severity: str      
    title: str
    evidence: str = ""


class BaseParser:
    """Interface every tool-specific parser must implement."""
    name = "base"

    def matches(self, command):
        """Return True if this parser should handle the given command."""
        raise NotImplementedError

    def parse_line(self, line: str) -> Optional[Finding]:
        """Parse a single line of tool output. Return a Finding or None."""
        raise NotImplementedError
