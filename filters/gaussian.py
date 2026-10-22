"""Gaussian filter untuk Gaussian Noise."""

import cv2
import numpy as np

from .common import DEFAULT_IMAGE, DEFAULT_OUTPUT, cli, read_image, save_comparison


def add_noise(image, sigma=20.0, seed=42):
    noise = np.random.default_rng(seed).normal(0, sigma, image.shape)
    return np.clip(image.astype(np.float32) + noise, 0, 255).astype(np.uint8)


def apply_filters(noisy):
    return [cv2.GaussianBlur(noisy, (k, k), 0) for k in (3, 5, 7)]


def main(image_path=DEFAULT_IMAGE, output_dir=DEFAULT_OUTPUT, show=True):
    """Mengurangi Gaussian Noise dengan Gaussian Blur."""
    image = read_image(image_path)
    noisy = add_noise(image)
    return save_comparison(
        [image, noisy, *apply_filters(noisy)],
        ["Citra asli (grayscale)", "Gaussian Noise", "Gaussian 3x3", "Gaussian 5x5", "Gaussian 7x7"],
        "gaussian_result.png", output_dir, show,
    )


if __name__ == "__main__":
    cli(main)
