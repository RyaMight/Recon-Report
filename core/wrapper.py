import os
import pty
import select
import subprocess
import sys


def run_and_capture(command, tool_parser, report_writer):

    master_fd, slave_fd = pty.openpty()

    proc = subprocess.Popen(
        command,
        stdout=slave_fd,
        stderr=slave_fd,
        close_fds=True
    )
    os.close(slave_fd)

    buffer = ""
    try:
        while True:
            ready, _, _ = select.select([master_fd], [], [], 0.1)
            if master_fd in ready:
                try:
                    data = os.read(master_fd, 4096).decode(errors="ignore")
                except OSError:
                    break
                if not data:
                    break

                sys.stdout.write(data)
                sys.stdout.flush()

                buffer += data
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    if tool_parser:
                        finding = tool_parser.parse_line(line)
                        if finding:
                            report_writer.append(finding)

            if proc.poll() is not None:
                break
    finally:
        os.close(master_fd)
        proc.wait()
