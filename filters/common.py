"""Pembacaan input dan visualisasi bersama untuk seluruh filter."""

import argparse
from pathlib import Path

import cv2
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_IMAGE = ROOT / "foto" / "tayama.jpg"
DEFAULT_OUTPUT = ROOT / "outputs"


def read_image(image_path=DEFAULT_IMAGE):
    path = Path(image_path).resolve()
    if not path.is_file():
        raise ValueError(f"Gambar input tidak ditemukan: {path}")
    image = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"Gambar tidak dapat dibaca: {path}. Gunakan file gambar yang valid.")
    print(f"Input: {path} | ukuran: {image.shape} | tipe data: {image.dtype}")
    return image


def save_comparison(images, titles, filename, output_dir=DEFAULT_OUTPUT, show=True):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    figure = plt.figure(figsize=(12, 4))
    try:
        for n, (image, title) in enumerate(zip(images, titles), start=1):
            plt.subplot(1, 5, n)
            plt.imshow(image, cmap="gray", vmin=0, vmax=255)
            plt.title(title, fontsize=9)
            plt.axis("off")
        plt.tight_layout()
        target = output_dir / filename
        plt.savefig(target, dpi=150)
        print(f"Tersimpan: {target.resolve()}")
        if show:
            plt.show()
        return target
    finally:
        plt.close(figure)


def cli(main):
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument("--image", type=Path, default=DEFAULT_IMAGE, help="Lokasi gambar input")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--no-show", action="store_true", help="Simpan PNG tanpa membuka jendela")
    args = parser.parse_args()
    try:
        main(image_path=args.image, output_dir=args.output_dir, show=not args.no_show)
    except (ValueError, OSError, cv2.error) as error:
        parser.exit(1, f"Error: {error}\n")
