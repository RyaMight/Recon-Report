# liverecon

**Stop wasting time writing pentest reports after the scan is done.**
`liverecon` wraps the tool you're already running — nmap, nuclei, and more
soon — and writes findings straight into a live Markdown report *while the
scan is still going*.

```bash
python cli.py wrap -- nmap -sV -p- target.com
```

Terminal output looks exactly the same as running the tool normally.
Meanwhile, `report.md` fills up in real time — open it side by side (VS Code
markdown preview, `tail -f`, whatever) and watch findings appear as the scan
runs.

## Why

Bug hunters lose hours after every engagement copy-pasting scan output into a
report. `liverecon` removes that step entirely: run your tools the way you
already do, and the report writes itself alongside you.

## Quick start

```bash
git clone <your-repo-url>
cd liverecon
python cli.py wrap --target acme-corp --report acme.md -- nmap -sV target.com
python cli.py wrap --target acme-corp --report acme.md -- nuclei -u https://target.com
```

Both runs above append to the **same** `acme.md`, so a full engagement builds
up into one report across multiple tools and multiple sessions.

## Supported tools (parsers)

| Tool | Status |
|---|---|
| nmap | ✅ |
| nuclei | ✅ |
| ffuf / gobuster | 🚧 planned |
| nikto | 🚧 planned |
| sslyze | 🚧 planned |

Adding a new tool is one file: implement `matches()` and `parse_line()` in
`parsers/base.py`'s `BaseParser` interface, then register it in
`parsers/__init__.py`.

## How it works

1. `wrap` runs your command inside a pseudo-terminal (`pty`), so colors and
   progress bars render exactly as normal.
2. Every line of output is also streamed to a tool-specific parser.
3. Matched findings are deduplicated and appended to the Markdown report as
   they happen — no waiting for the tool to finish.

## Requirements

- Python 3.8+
- Linux or macOS (uses the `pty` module, not available on Windows)

## Roadmap

- [ ] More parsers (ffuf, gobuster, nikto, sslyze, subfinder)
- [ ] `--watch` mode for tools that only write to a file (e.g. `nmap -oX`)
- [ ] Optional local web dashboard with live WebSocket updates
- [ ] Severity-based summary section auto-generated at the top of the report
- [ ] Export to PDF/HTML from the accumulated Markdown

## Contributing

New parsers are the easiest way to contribute — see `parsers/nmap.py` for a
minimal example. PRs welcome.

## License

MIT
