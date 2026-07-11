import re
from .base import BaseParser, Finding

PORT_LINE = re.compile(r"^(\d+)/(tcp|udp)\s+(open|filtered)\s+(\S+)(?:\s+(.*))?$")
HOST_LINE = re.compile(r"^Nmap scan report for (.+)$")


class NmapParser(BaseParser):
    name = "nmap"

    def matches(self, command):
        return bool(command) and "nmap" in command[0]

    def parse_line(self, line):
        line = line.strip()

        host_match = HOST_LINE.match(line)
        if host_match:
            return Finding(
                tool=self.name,
                severity="info",
                title=f"Host discovered: {host_match.group(1)}",
                evidence=""
            )

        port_match = PORT_LINE.match(line)
        if port_match:
            port, proto, state, service, version = port_match.groups()
            title = f"Port {port}/{proto} {state} — {service}"
            evidence = version.strip() if version else ""
            return Finding(
                tool=self.name,
                severity="info" if state == "open" else "low",
                title=title,
                evidence=evidence
            )

        return None
