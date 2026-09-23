"""Pull NYC TLC yellow taxi trip records for a range of months and store them as CSV.

Usage:
    uv run pull_trip_data --from 2022-02 --to 2023-03 [--out-dir data/raw]
"""

import argparse
import logging
from datetime import date
from pathlib import Path

import pandas as pd

BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"
DEFAULT_OUT_DIR = Path("data/raw")

logger = logging.getLogger(__name__)


def month_range(start: str, end: str) -> list[date]:
    """Return the first day of every month from `start` to `end` (inclusive), both in YYYY-MM format."""
    current = date.fromisoformat(f"{start}-01")
    last = date.fromisoformat(f"{end}-01")
    if current > last:
        raise ValueError(f"--from ({start}) must not be after --to ({end})")

    months = []
    while current <= last:
        months.append(current)
        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1)
        else:
            current = current.replace(month=current.month + 1)
    return months


def pull_month(month: date, out_dir: Path) -> Path:
    name = f"yellow_tripdata_{month:%Y-%m}"
    df = pd.read_parquet(f"{BASE_URL}/{name}.parquet")
    out_path = out_dir / f"{name}.csv"
    df.to_csv(out_path, index=False)
    return out_path


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--from", dest="start", required=True, help="first month to pull (YYYY-MM)")
    parser.add_argument("--to", dest="end", required=True, help="last month to pull, inclusive (YYYY-MM)")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR, help=f"default: {DEFAULT_OUT_DIR}")
    args = parser.parse_args()

    try:
        months = month_range(args.start, args.end)
    except ValueError as e:
        parser.error(str(e))

    print(f"will download from {args.start} to {args.end} ({len(months)} files)", flush=True)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for month in months:
        print(f"downloading {month:%Y-%m}", flush=True)
        try:
            out_path = pull_month(month, args.out_dir)
            logger.info("%s: saved to %s", f"{month:%Y-%m}", out_path)
        except Exception as e:
            logger.error("%s: failed to pull: %s", f"{month:%Y-%m}", e)
    print("done", flush=True)


if __name__ == "__main__":
    main()
