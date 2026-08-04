"""Input/output helpers for government workbooks and derived artifacts."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd

AIR_QUALITY_REQUIRED = {
    "From Date",
    "To Date",
    "Ozone",
    "CO",
    "SO2",
    "NO2",
    "PM10",
    "PM2.5",
    "State",
    "City",
    "Station",
}


def read_air_quality_workbook(path: str | Path, expected_state: str | None = None) -> pd.DataFrame:
    """Read and minimally validate one CPCB-style workbook."""
    source = Path(path)
    if not source.exists():
        raise FileNotFoundError(f"Air-quality workbook not found: {source}")
    frame = pd.read_excel(source)
    missing = AIR_QUALITY_REQUIRED.difference(frame.columns)
    if missing:
        raise ValueError(f"{source.name} is missing required columns: {sorted(missing)}")
    frame = frame.copy()
    frame["source_file"] = source.name
    frame["expected_state"] = expected_state
    return frame


def read_air_quality_collection(raw_dir: str | Path, state_files: dict[str, str]) -> pd.DataFrame:
    """Read and concatenate configured state workbooks."""
    base = Path(raw_dir)
    frames = [read_air_quality_workbook(base / filename, state) for state, filename in state_files.items()]
    if not frames:
        raise ValueError("No air-quality workbooks were configured.")
    return pd.concat(frames, ignore_index=True)


def list_source_files(path: str | Path, patterns: Iterable[str] = ("*.xls", "*.xlsx", "*.csv")) -> pd.DataFrame:
    """Return an inventory of source files without changing them."""
    directory = Path(path)
    records: list[dict[str, object]] = []
    if not directory.exists():
        return pd.DataFrame(columns=["file_name", "extension", "size_bytes", "path"])
    for pattern in patterns:
        for item in sorted(directory.glob(pattern)):
            records.append(
                {
                    "file_name": item.name,
                    "extension": item.suffix.lower(),
                    "size_bytes": item.stat().st_size,
                    "path": item.as_posix(),
                }
            )
    return pd.DataFrame(records).drop_duplicates(subset=["path"]).reset_index(drop=True)


def write_csv(frame: pd.DataFrame, path: str | Path) -> Path:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(destination, index=False)
    return destination
