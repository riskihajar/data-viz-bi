from __future__ import annotations

import argparse
import shutil
import sys
import zipfile
from pathlib import Path
from urllib.request import urlopen


DEFAULT_URL = "https://analyse.kmi.open.ac.uk/open-dataset/download"
DEFAULT_FILENAME = "anonymisedData.zip"
EXPECTED_EXTRACTED_FILES = {
    "assessments.csv",
    "courses.csv",
    "studentAssessment.csv",
    "studentInfo.csv",
    "studentRegistration.csv",
    "studentVle.csv",
    "vle.csv",
}


def download_file(url: str, destination: Path, force: bool = False) -> None:
    if destination.exists() and not force:
        print(f"Skip download, file already exists: {destination}")
        return

    destination.parent.mkdir(parents=True, exist_ok=True)
    tmp_destination = destination.with_suffix(destination.suffix + ".part")

    with urlopen(url) as response, open(tmp_destination, "wb") as f:
        shutil.copyfileobj(response, f)

    tmp_destination.replace(destination)
    print(f"Downloaded: {destination}")


def extract_zip(zip_path: Path, extract_dir: Path, force: bool = False) -> None:
    extract_dir.mkdir(parents=True, exist_ok=True)

    if not force and EXPECTED_EXTRACTED_FILES.issubset({p.name for p in extract_dir.iterdir()}):
        print(f"Skip extract, dataset files already exist in: {extract_dir}")
        return

    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(extract_dir)

    print(f"Extracted to: {extract_dir}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download and extract OULAD dataset")
    parser.add_argument("--url", default=DEFAULT_URL, help="Dataset download URL")
    parser.add_argument(
        "--output-dir",
        default=str(Path(__file__).resolve().parents[1] / "data" / "oulad"),
        help="Directory to store the zip file and extracted CSV files",
    )
    parser.add_argument(
        "--filename",
        default=DEFAULT_FILENAME,
        help="Zip filename to save inside output directory",
    )
    parser.add_argument(
        "--no-extract",
        action="store_true",
        help="Download only, do not extract the zip archive",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-download and re-extract even if files already exist",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir).expanduser().resolve()
    zip_path = output_dir / args.filename

    try:
        download_file(args.url, zip_path, force=args.force)
        if not args.no_extract:
            extract_zip(zip_path, output_dir, force=args.force)
    except Exception as exc:  # pragma: no cover - CLI guard
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print("OULAD dataset is ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
