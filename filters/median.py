"""Median Filter 3x3 untuk Salt and Pepper Noise."""

import cv2

from .common import DEFAULT_IMAGE, DEFAULT_OUTPUT, add_noise, cli, run_filter

COMPARISON = 'perbandingan_median.png'

def apply_filters(noisy):
    return [cv2.medianBlur(noisy, 3)]


def main(image_path=DEFAULT_IMAGE, output_dir=DEFAULT_OUTPUT, show=True):
    """Median Filter 3x3 untuk Salt and Pepper Noise."""
    return run_filter(image_path, output_dir, show, apply_filters,
                      ['Hasil Median Filter'],
                      ['hasil_mf.png'], COMPARISON)


if __name__ == "__main__":
    cli(main)
