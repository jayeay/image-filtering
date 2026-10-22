"""Low Pass Filter sesuai materi praktikum."""

import cv2
import numpy as np

from .common import DEFAULT_IMAGE, DEFAULT_OUTPUT, add_noise, cli, run_filter

COMPARISON = 'perbandingan_lpf.png'

KERNELS = (
    np.array([[1/16, 1/8, 1/16], [1/8, 1/4, 1/8], [1/16, 1/8, 1/16]], dtype=np.float32),
    np.array([[1/10, 1/10, 1/10], [1/10, 1/5, 1/10], [1/10, 1/10, 1/10]], dtype=np.float32),
    np.ones((3, 3), dtype=np.float32) / 9,
)


def apply_filters(noisy):
    responses = [cv2.filter2D(noisy, cv2.CV_32F, kernel,
                             borderType=cv2.BORDER_CONSTANT) for kernel in KERNELS]
    return [np.clip(np.rint(result), 0, 255).astype(np.uint8) for result in responses]


def main(image_path=DEFAULT_IMAGE, output_dir=DEFAULT_OUTPUT, show=True):
    """Low Pass Filter sesuai materi praktikum."""
    return run_filter(image_path, output_dir, show, apply_filters,
                      ['LPF 1: Berbobot', 'LPF 2: Pusat 1/5', 'LPF 3: Rata-rata'],
                      ['hasil_lpf1.png', 'hasil_lpf2.png', 'hasil_lpf3.png'], COMPARISON)


if __name__ == "__main__":
    cli(main)
