"""Validate the local fire-detect dataset layout for YOLOv5 training."""

from __future__ import annotations

import argparse
from pathlib import Path

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}
EXPECTED_CLASS_COUNT = 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate YOLO fire dataset splits and labels.")
    parser.add_argument("--dataset", type=Path, default=Path("datasets/fire-detect-1"))
    return parser.parse_args()


def count_images(path: Path) -> int:
    return sum(1 for item in path.iterdir() if item.is_file() and item.suffix.lower() in IMAGE_SUFFIXES)


def validate_split(root: Path, split: str) -> tuple[int, int, list[str]]:
    images_dir = root / split / "images"
    labels_dir = root / split / "labels"
    errors: list[str] = []

    if not images_dir.exists():
        errors.append(f"Missing {images_dir}")
        return 0, 0, errors
    if not labels_dir.exists():
        errors.append(f"Missing {labels_dir}")
        return count_images(images_dir), 0, errors

    images = [p for p in images_dir.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES]
    labels = [p for p in labels_dir.iterdir() if p.is_file() and p.suffix.lower() == ".txt"]
    label_names = {p.stem for p in labels}

    for image in images:
        if image.stem not in label_names:
            errors.append(f"Missing label for {split}/images/{image.name}")

    for label in labels:
        for line_no, line in enumerate(label.read_text(encoding="utf-8").splitlines(), start=1):
            stripped = line.strip()
            if not stripped:
                continue
            parts = stripped.split()
            if len(parts) != 5:
                errors.append(f"{label}: line {line_no} should have 5 YOLO fields")
                continue
            class_id = int(float(parts[0]))
            if class_id < 0 or class_id >= EXPECTED_CLASS_COUNT:
                errors.append(f"{label}: line {line_no} has invalid class id {class_id}")

    return len(images), len(labels), errors


def main() -> int:
    args = parse_args()
    root = args.dataset
    all_errors: list[str] = []

    for split in ("train", "valid", "test"):
        image_count, label_count, errors = validate_split(root, split)
        print(f"{split}: {image_count} images, {label_count} labels")
        all_errors.extend(errors)

    if all_errors:
        print("\nErrors:")
        for error in all_errors[:50]:
            print(f"- {error}")
        if len(all_errors) > 50:
            print(f"- ... {len(all_errors) - 50} more")
        return 1

    print("Dataset layout looks valid for a single-class fire detector.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
