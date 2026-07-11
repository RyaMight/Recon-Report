from datetime import datetime


class ReportWriter:


    def __init__(self, session):
        self.session = session
        self.path = session.report_path
        self._seen = set()  

    def log_command(self, command):
        cmd_str = " ".join(command)
        with open(self.path, "a") as f:
            f.write(f"## Run: `{cmd_str}`\n")
            f.write(f"_{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n\n")
        print(f"[liverecon] Logging to {self.path} ...\n")

    def append(self, finding):
        key = (finding.tool, finding.title, finding.evidence)
        if key in self._seen:
            return
        self._seen.add(key)

        with open(self.path, "a") as f:
            f.write(f"- **[{finding.severity.upper()}]** {finding.title}")
            if finding.evidence:
                f.write(f" — `{finding.evidence}`")
            f.write("\n")

    def close_command(self):
        with open(self.path, "a") as f:
            f.write("\n---\n\n")
        print(f"[liverecon] Done. Report updated: {self.path}")
