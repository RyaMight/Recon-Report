import os
from datetime import datetime


class Session:
    def __init__(self, target=None, report_path="report.md"):
        self.target = target or "session"
        self.report_path = report_path
        self.started_at = datetime.now()

        if not os.path.exists(self.report_path):
            self._init_report()

    def _init_report(self):
        with open(self.report_path, "w") as f:
            f.write(f"# Live Recon Report — {self.target}\n\n")
            f.write(f"_Started: {self.started_at.strftime('%Y-%m-%d %H:%M:%S')}_\n\n")
            f.write("---\n\n")
