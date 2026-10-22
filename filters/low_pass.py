"""Low Pass Filter dengan tiga kernel rata-rata."""

import cv2
import numpy as np

from .common import DEFAULT_IMAGE, DEFAULT_OUTPUT, cli, read_image, save_comparison


def apply_filters(image):
    return [cv2.filter2D(image, -1, np.ones((k, k), np.float32) / (k * k))
            for k in (3, 5, 7)]


def main(image_path=DEFAULT_IMAGE, output_dir=DEFAULT_OUTPUT, show=True):
    """Menghaluskan citra menggunakan LPF 3x3, 5x5, dan 7x7."""
    image = read_image(image_path)
    return save_comparison(
        [image, image.copy(), *apply_filters(image)],
        ["Citra asli (grayscale)", "Input grayscale", "LPF 3x3", "LPF 5x5", "LPF 7x7"],
        "lpf_result.png", output_dir, show,
    )


if __name__ == "__main__":
    cli(main)
