"""Median filter untuk Salt and Pepper Noise."""

import cv2
import numpy as np

from .common import DEFAULT_IMAGE, DEFAULT_OUTPUT, cli, read_image, save_comparison


def add_noise(image, amount=0.05, seed=42):
    if not 0 <= amount <= 1:
        raise ValueError("Proporsi noise harus berada dalam rentang 0 hingga 1.")
    noisy = image.copy()
    mask = np.random.default_rng(seed).random(image.shape)
    noisy[mask < amount / 2] = 0
    noisy[mask >= 1 - amount / 2] = 255
    return noisy


def apply_filters(noisy):
    return [cv2.medianBlur(noisy, k) for k in (3, 5, 7)]


def main(image_path=DEFAULT_IMAGE, output_dir=DEFAULT_OUTPUT, show=True):
    """Mengurangi Salt and Pepper Noise dengan median filter."""
    image = read_image(image_path)
    noisy = add_noise(image)
    return save_comparison(
        [image, noisy, *apply_filters(noisy)],
        ["Citra asli (grayscale)", "Salt and Pepper Noise", "Median 3x3", "Median 5x5", "Median 7x7"],
        "median_result.png", output_dir, show,
    )


if __name__ == "__main__":
    cli(main)
