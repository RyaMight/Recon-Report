import re
from .base import BaseParser, Finding

NUCLEI_LINE = re.compile(
    r"^\[([^\]]+)\]\s*\[([^\]]+)\]\s*\[([^\]]+)\]\s*(\S+)"
)

SEVERITY_MAP = {"info", "low", "medium", "high", "critical", "unknown"}


class NucleiParser(BaseParser):
    name = "nuclei"

    def matches(self, command):
        return bool(command) and "nuclei" in command[0]

    def parse_line(self, line):
        line = line.strip()
        match = NUCLEI_LINE.match(line)
        if not match:
            return None

        template_id, protocol, severity, target = match.groups()
        severity = severity.lower() if severity.lower() in SEVERITY_MAP else "unknown"

        return Finding(
            tool=self.name,
            severity=severity,
            title=f"{template_id} ({protocol})",
            evidence=target
        )
