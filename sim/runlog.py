"""JSONL run log (WORLD_SPEC section 8). One file per run, written line by line
and flushed, so a crash still leaves every line written before it."""

import copy
import json
from pathlib import Path


def dumps(record):
    return json.dumps(record, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


class RunLog:
    def __init__(self, path=None):
        self.path = Path(path) if path else None
        self.records = []
        self._fh = None
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self._fh = open(self.path, "w", encoding="utf-8", newline="\n")

    def write(self, type_, **fields):
        record = {"seq": len(self.records), "type": type_, **fields}
        line = dumps(record)
        # Keep the JSON round-tripped copy so in-memory records equal the file.
        self.records.append(json.loads(line))
        if self._fh:
            self._fh.write(line + "\n")
            self._fh.flush()

    def close(self):
        if self._fh:
            self._fh.close()
            self._fh = None


def read_log(path):
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def strip_perf(records):
    """Drop wall-clock fields, which are the only non-deterministic content."""
    out = []
    for record in records:
        record = copy.deepcopy(record)
        record.pop("perf", None)
        out.append(record)
    return out
