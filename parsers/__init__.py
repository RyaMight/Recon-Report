from .nmap import NmapParser
from .nuclei import NucleiParser

_PARSERS = [NmapParser(), NucleiParser()]


def get_parser_for_command(command):
    for parser in _PARSERS:
        if parser.matches(command):
            return parser
    return None  # fallback: tetap tampil di terminal, tapi tidak di-parse ke report
