#!/usr/bin/env python3
import argparse
import sys

from core.wrapper import run_and_capture
from core.report_writer import ReportWriter
from core.session import Session
from parsers import get_parser_for_command


def main():
    parser = argparse.ArgumentParser(
        prog="liverecon",
        description="Live report generator that runs alongside your recon tools."
    )
    subparsers = parser.add_subparsers(dest="action", required=True)

    wrap_parser = subparsers.add_parser(
        "wrap",
        help="Wrap a tool command and stream findings into the live report."
    )
    wrap_parser.add_argument(
        "--target", help="Target/session name (default: 'session')."
    )
    wrap_parser.add_argument(
        "--report", default="report.md",
        help="Path to the markdown report file (default: report.md)."
    )

    args, remainder = parser.parse_known_args()

    if args.action == "wrap":
        if "--" in remainder:
            idx = remainder.index("--")
            command = remainder[idx + 1:]
        else:
            command = remainder

        if not command:
            print(
                "Error: no command provided after --.\n"
                "Example:\n"
                "  python cli.py wrap -- nmap -sV -p- target.com"
            )
            sys.exit(1)

        session = Session(target=args.target, report_path=args.report)
        report_writer = ReportWriter(session)
        tool_parser = get_parser_for_command(command)

        if tool_parser is None:
            print(
                f"[liverecon] No parser matched for '{command[0]}'. "
                "Output will still stream to terminal, but nothing will "
                "be written to the report.\n"
            )

        report_writer.log_command(command)
        run_and_capture(command, tool_parser, report_writer)
        report_writer.close_command()


if __name__ == "__main__":
    main()
