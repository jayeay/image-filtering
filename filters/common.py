"""Pembacaan input dan visualisasi bersama untuk seluruh filter."""

import argparse
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_IMAGE = ROOT / "images" / "living.jpg"
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
    figure = plt.figure(figsize=(12, 8) if len(images) == 3 else (12, 4))
    try:
        for n, (image, title) in enumerate(zip(images, titles), start=1):
            plt.subplot(1, len(images), n)
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


def add_noise(image, seed=42):
    """Salt and Pepper Noise: probabilitas hitam 2%, putih 2%."""
    noisy = image.copy()
    noise_mask = np.random.default_rng(seed).random(image.shape[:2])
    noisy[noise_mask < 0.02] = 0
    noisy[noise_mask > 0.98] = 255
    return noisy


def run_filter(image_path, output_dir, show, apply_filters, titles, filenames, comparison):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    image = read_image(image_path)
    noisy = add_noise(image)
    results = apply_filters(noisy)
    paths = []
    for result, filename in zip(results, filenames):
        path = output_dir / filename
        if not cv2.imwrite(str(path), result):
            raise OSError(f"Tidak dapat menyimpan citra: {path}")
        print(f"Tersimpan: {path.resolve()}")
        paths.append(path)
    save_comparison([image, noisy, *results], ["Citra Asli", "Citra Noisy", *titles],
                    comparison, output_dir, show)
    return paths
