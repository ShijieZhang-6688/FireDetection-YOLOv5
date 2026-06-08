"""Download the Roboflow fire-detect dataset used for this reproduction.

The exact dataset is:
https://universe.roboflow.com/yolo-j5nit/fire-detect-i7huf-0g2xe/dataset/1

Set ROBOFLOW_API_KEY before running:
    $env:ROBOFLOW_API_KEY="..."
    python scripts/download_dataset.py
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

import requests


WORKSPACE = "yolo-j5nit"
PROJECT = "fire-detect-i7huf-0g2xe"
VERSION = "1"
FORMAT = "yolov5pytorch"
DEFAULT_OUTPUT = Path("datasets/fire-detect-1")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download the Roboflow fire-detect dataset.")
    parser.add_argument("--api-key", default=os.getenv("ROBOFLOW_API_KEY"), help="Roboflow API key.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Dataset output directory.")
    return parser.parse_args()


def download_zip(api_key: str, target_zip: Path) -> None:
    url = f"https://api.roboflow.com/{WORKSPACE}/{PROJECT}/{VERSION}/{FORMAT}"
    params = {"api_key": api_key}
    with requests.get(url, params=params, timeout=120) as response:
        response.raise_for_status()
        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type:
            export = response.json().get("export", {})
            download_url = export.get("link")
            if not download_url:
                raise RuntimeError("Roboflow response did not include export.link.")
        else:
            download_url = response.url

    with requests.get(download_url, stream=True, timeout=120) as response:
        response.raise_for_status()
        with target_zip.open("wb") as fh:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    fh.write(chunk)


def unpack_dataset(zip_path: Path, output_dir: Path) -> None:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as archive:
        archive.extractall(output_dir)


def main() -> int:
    args = parse_args()
    if not args.api_key:
        print("ROBOFLOW_API_KEY is required. Create one in Roboflow, then rerun this script.", file=sys.stderr)
        return 2

    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = Path(tmpdir) / "fire-detect-1.zip"
        print(f"Downloading Roboflow dataset {WORKSPACE}/{PROJECT}:{VERSION} ...")
        download_zip(args.api_key, zip_path)
        print(f"Extracting to {args.output} ...")
        unpack_dataset(zip_path, args.output)

    print("Done. Validate with: python scripts/validate_dataset.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
