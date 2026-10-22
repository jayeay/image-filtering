"""Gaussian Filter 3x3, sigmaX=1.0, untuk Salt and Pepper Noise."""

import cv2

from .common import DEFAULT_IMAGE, DEFAULT_OUTPUT, add_noise, cli, run_filter

COMPARISON = 'perbandingan_gaussian.png'

def apply_filters(noisy):
    return [cv2.GaussianBlur(noisy, (3, 3), sigmaX=1.0)]


def main(image_path=DEFAULT_IMAGE, output_dir=DEFAULT_OUTPUT, show=True):
    """Gaussian Filter 3x3, sigmaX=1.0, untuk Salt and Pepper Noise."""
    return run_filter(image_path, output_dir, show, apply_filters,
                      ['Hasil Gaussian Filter'],
                      ['hasil_gf.png'], COMPARISON)


if __name__ == "__main__":
    cli(main)
